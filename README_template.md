{{toc}}

# Goals

PowerBI is one of the top visualization tools out there. However, it lacks a number of data adminstration-type abilities. The goal of this project is to fill some of these holes, such as:

1. Creating a low-level python interface with PowerBI's SSAS backend. Specifically, we'd like people to be able to schedule local data refreshes. We'd also like to expose the DataModel's schema as a JSON without needing to think about SSAS.
2. Identifying report lineage. Some reports are frankensteined from previous reports. We hope to be able use the table, datasource, measure, and visual IDs to identify reports that share a relationship
3. Allowing people to query PBIX datamodel information with SQL
4. Creating a tool for analysts to allow them to view reports using the same datasources/measures as they are.
5. A data lineage tool for DEs allowing them to connect datasources to individual visuals in each report.

# Details

[Extract Lib](lib/README.md)

[Schema Parser](load_to_db/README.md)

[Schema Visualizer](visualizer/README.md)

# Set Up

```
pip install -r requirements.txt
cd lib
python setup.py sdist
```

# Dev extras

Has a black pre-commit hook

```
git config core.hooksPath hooks
```

# Demo

Uses a docker image
`docker build . -t demo`
`docker run -p 22:22 -p 100:100 -p 5000:5000 -p 5433:5432 demo`


# Help
Expressions are DAX-generated tables

Don't understand `ExtendedProperty`, see `Income share held by lowest 20%` in `c:/Users/mwham/Documents/repos/powerbi-decompressor/pbis/Life expectancy v202009.pbix`

Don't understand variations, see `c:/Users/mwham/Documents/repos/powerbi-decompressor/pbis/Sales & Returns Sample v201912.pbix`