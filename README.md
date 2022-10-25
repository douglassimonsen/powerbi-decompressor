# Goal

Data lineage is important, but it's focused in the data engineer's world with tools like DBT. This is despite the fact that analysts are often the messiest data people. One big issue with tracking data lineage through to the final reports is the PowerBI is a black box. 

Although the .pbix is a simple zip file, the core data structures are stored in a DataModel file within the zip file. The DataModel file is compressed with XPress9, which appears to be different from the XPress algorithm. In any case, this compression is essentially undocumented and there are no simple utilities for decompressing the file.

Therefore, to get the data out of the PowerBI, we take a somewhat circuitous route. We instantiate a Microsoft Analysis Server locally, sending XMLA commands to load/save the PowerBI. 

# Example
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


netstat -ab | findstr msmd