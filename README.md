# Goal

Data lineage is important, but it's focused in the data engineer's world with tools like DBT. This is despite the fact that analysts are often the messiest data people. One big issue with tracking data lineage through to the final reports is the PowerBI is a black box. 

Although the .pbix is a simple zip file, the core data structures are stored in a DataModel file within the zip file. The DataModel file is compressed with XPress9, which appears to be different from the XPress algorithm. In any case, this compression is essentially undocumented and there are no simple utilities for decompressing the file.

Therefore, to get the data out of the PowerBI, we take a somewhat circuitous route. We instantiate a Microsoft Analysis Server locally, sending XMLA commands to load/save the PowerBI. 

# Journey

The core issue with programmatically accessing PowerBI data is that the `/DataModel` file is compressed with the  XPRESS9 algorithm. When searched online, you'll find [this](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/fccm2014kim_cr.pdf) paper and 100's of engineers asking how to decompress *pbix* with people answering "this is how to extract it from *pbit*". After getting an unhelpful response from the researchers in the paper, we explore other options.

The first avenue was using [dotpeek](https://www.jetbrains.com/decompiler/) to extract the source code from the `powerbi.exe` file to replicate the compression algorithm. Sadly it turns out, the algorithm is in another castle. PowerBI uses a SSAS instance on the backend to manage the data and does no compression/decompression itself. With some more code spelunking, I was able to decypher how PowerBI instantiates and communicates with the SSAS service.

For reference, 
1. `powerbi.exe` links to the DLL `Microsoft.PowerBI.Client`. 
2. In the program function, an instance of `IAnalysisServicesService` is instantiated (see below for partial source)
3. This class is implemented in `Microsoft.PowerBI.Client.Windows.AnalysisServices.AnalysisServicesService`
4. Within this class are two functions that we care about (see below for source)
    - `CreateDatabase`
    - `LoadDatabaseFromPbix`
5. Going through the layers of code in these two functions becomes fuzzy due to the Injection-heavy code. However, two things become apparent:
    - Most of the configs, etc. connecting PowerBI to SSAS is stored in a folder named `C:\Users\[username]\AppData\Local\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces\AnalysisServicesWorkspace_[GUID]\Data`
    - All communications between the two services go through XMLA
6. Going into the folder, SSAS thankfully provides us with a trace file (`FlightRecorderCurrent.trc`) that records every XMLA command sent to SSAS. Copying and editing these commands (see `/xmla`), we can load our own .pbix files and automatically retrieve the information in `/DataModel`! 
7. The final step involve(s/d) looking through another section of the source code to identify:
    - the exact executable running SSAS
    - the command line arguments PowerBI supplies to the executable
    - the initial XMLA commands PowerBI sends to enable PowerBI specific functionality

![main program](documents/program_analysis_services.png)

![Analysis Services](documents/analysis_services_db.png)

![Trace File](documents/trace_file.png)

Note: all DLLs can be found in `C:\Program Files\Microsoft Power BI Desktop\bin`

# How it works
## Initialization
Initialization first checks if there is an existing Workspace. If there is, it checks whether the corresponding port is an active SSAS instance by attempting to query a list of databases in the instance. If there are no workspaces with a corresponding active SSAS instance, the program attempts to generate its own SSAS instance.

To create its own instance, the library generates a random UUID4, creates a corresponding workspace, and runs the command:

`'C:\Program Files\Microsoft Power BI Desktop\bin\msmdsrv.exe' "-c" "-n" {self.instance_name()} -s {self.data_directory()}`

It then iterates over every process currently running to find one with the name `msmdsrv.exe`.

It then gets the port of the first socket associated with that executable, saving that value to `msmdsrv.port.txt` to match PowerBI-generated workspaces.

[WIP] we then run [create_db](xmla/create_db.xml) to generate a database to load to with the appropriate permissions and PowerBI-specific extensions

## Loading PBIX to SSAS

We simply run [image_load](xmla/image_load.xml) with the appropriate values

## Saving PBIX from SSAS

Since the SSAS instance only saves a `/DataModel` and can only save files to the workspace, this has a few steps:

1. Copy PBIX to workspace
2. Run [image_save](xmla/image_save.xml) to update the PBIX `/DataModel`
3. Move the workspace PBIX to the intended save location

## Extracting Schema

After loading the PBIX to SSAS, we simply run [schema_query](xmla/schema_query.xml), returning an XML. We then run a simple process to convert that XML to JSON.

[WIP] We then use [lark](https://lark-parser.readthedocs.io/en/latest/) to implement a [grammar](dax_parser.py) for DAX(MDX?), allowing us to parse the source information to identify the type/details of source as well as any additional manipulations being done to it.

# Examples

## Getting Schema Information
```
from powerbi import PowerBI
pbi = PowerBI('test.pbix')
pbi.load_image()
pbi.save_image('test2.pbix')  # currently not that valuable, since there are no updates
schema = pbi.read_schema()
print(schema)
```
```
  {
    "Model": {},
    "DataSource": {},
    "Table": {},
    "Column": {},
    "AttributeHierarchy": {},
    "Partition": {},
    "Relationship": {},
    "Measure": {},
    "Hierarchy": {},
    "Level": {},
    "Annotation": {},
    ...
}
```

## Updating Tables

```
from powerbi import PowerBI
pbi = PowerBI('test.pbix')
pbi.update_tables()
```