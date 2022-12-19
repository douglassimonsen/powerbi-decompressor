# Schema

Visuals depend on measures or columns (possibly calculated)
Measures and columns depend on tables
Tables (generally) depend on outside datasources

## Parsed Fields

## Annotations

Summary: Annotations are notes about another element in the PBIX. As far as I can tell, all PBIX objects are candidates for an annotation. You can see a list of decrypted ID mappings for objects in [Annotation Object Types](#annotation-object-types).

### Examples

```
select name, value from pbi.annotations
```
| name | value |
| ---- | ----- |
| DataTypeAtRefresh	| Int64#####not a type |
| SummarizationSetBy | User |
| Format | \<Format Format="DateTimeGeneralPattern"\>\<DateTimes\>\<DateTime LCID="1033" Group="GeneralDateTimeLong" FormatString="G" />\</DateTimes>\</Format\> |

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |
| object_type | [Annotation Object Types](#annotation-object-types) |

### Sample Queries

Getting all annotations related to columns

```
select c.*, a.* 
from pbi.annotations a

inner join pbi.annotation_object_types aot 
on a.object_type = aot.id 

inner join pbi."columns" c 
on a.object_id = c.id::text

where aot.name = 'column'
```

## Columns

Summary: Columns are the columns in PBI tables after powerquery renaming. They contain information about the data type. If the `Expression` field is non-null, the column is calculated. There are other fields which I haven't seen in PowerBI (`isKey`, `State`, etc.) that still need decoding, but may legacy fields for SSAS. 

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| table_id | [Tables](#tables) |
| data_type | [Datatypes](#datatypes) |

Foreign Keys From: 

| Column | Table |
| ------ | ----- |
| from_column_id | [Relationships](#relationships) |
| to_column_id | [Relationships](#relationships) |
| column_id | [Levels](#levels) |
| hierarchy_column_id | [Levels](#levels) |

## Data Sources

Summary: Contains information about how to connect to external data sources during updates. Although may theoretically be able to connect to multiple partitions, appears to be de facto 1-to-1 with [Partitions](#partitions). Also contains `max_connections`, which may control parallelization when refreshing data sources.

### Examples 

```
provider=Microsoft.PowerBI.OleDb;global pipe=f777e697-9c9c-482a-8a19-aa356190386d;mashup=\"<Base64 Binary(?)>\";location=Sales
```

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |

Foreign Keys From: 

| Column | Table |
| ------ | ----- |
| data_source_id | [Partitions](#partitions) |


## Expressions

Summary: Looks like an alternative way to access external data. Unsure of whay it looks like on the PBI side.


### Examples

```
"POWERBI-SQL" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

```
(Page as number) =>
let
    Source = Xml.Tables(Web.Contents("https://api.worldbank.org/v2/country?page="&Number.ToText(Page))),
    country = Source{0}[country]
in
    country
```

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |

## Hierarchies

Summary: Is the container around hierarchy elements. In the most common example, imagine a column `Column A` with a `Date Hierarchy` containing `day`, `month`, `year`, the `Date Hierarchy` would be an element of this table. Not very useful in itself, since most references go to the column `Column A`. 

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| table_id | [Tables](#tables) |

Foreign Keys From: 

| Column | Table |
| ------ | ----- |
| hierarchy_id | [Levels](#levels) |

## Levels

### Example

```
Column A
  Date Hierarchy
    -Day
    -Month
    -Year
would have records for day, month, and year. Each would have foreign keys to:

Day, Month, Year Columns (through column_id)

Date Hierarchy (through hierarchy_id)

Column A (through hierarchy_column_id)
```

Summary: In the description of hierarchy in [Hierarchies](#hierarchies), this table would contain the `day`, `month`, and `year`. Each element has a corresponding column, referenced through `column_id`. The `hierarchy_column_id` is the column containing the hierarchy, `Column A` in the case of the example.

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| column_id | [Columns](#columns) |
| hierarchy_column_id | [Columns](#columns) |
| hierarchy_id | [Hierarchies](#hierarchies) |

## Linguistic Metadata

Summary: contains information about the language of the report and contains information converting semantic entities to various specific languages. Not meaningfully implemented on examples I've seen.

### Example

```
[{"name": "sale", "words": ["sale table"], "source": "Generated", "conceptual_entity": "Sales"}, {"name": "sale.property", "words": ["."], "source": "Generated", "conceptual_entity": "Sales"}, {"name": "sale.a_report_link", "words": ["a report link"], "source": "Generated", "conceptual_entity": "Sales"}, {"name": "sale.brand_name", "words": ["brand name"], "source": "Generated", "conceptual_entity": "Sales"}, {"name": "sale.category", "words": ["category"], "source": "Generated", "conceptual_entity": "Sales"}]
```

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |

## Measures

Summary: Contains all measures in a PBIX. Contains actual expression and the resulting data type

### Example
```
Name: SalesAmount average per Country

Expression: AVERAGEX(
	KEEPFILTERS(VALUES('Sales'[Country])),
	CALCULATE(SUM('Sales'[SalesAmount]))
)

Data Type: Decimal Number
```

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| data_type | [Data Types](#datatypes) |
| table_id | [Tables](#tables) |

## Pages

Summary: Information about each visual page in a PBIX report. There are also some edge cases such as popouts and summary pages that don't cleanly map to a "page" idea included in this table. They can often be identified by their non-standard display sizes.

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| page_id | [Visuals](#visuals) |

## Partitions

Summary: Partitions contain details about external/source datasets. In some cases, the datasets are just generated information, such as `Calendar(Date(2015,1,1), Date(2015,1,1))`. In these cases, there is no associated data_source_id. 

This library is attempting to parse the query_definition to get more detailed information about the sources. Currently the parsing can extract information about `Sql.Database`, `Excel.Workbook`, and `CSV.Document`.

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| data_source_id | [Data Sources](#data-sources) |
| table_id | [Tables](#tables) |

## Relationships

Summary: this table contains information about how cross-filtering a given table will impact other tables. This table powers the `Model` tab in a PBIX report. I'm unsure what inactive relationships look like. Each relationship can be (1/Many) to (1/Many) and cross_filtering can be left-to-right or bidrectional. There's an option to "Rely on Referential Integrity" which may allow improved performance

### Example

```
From Column Id: 2072
From Cardinality: 2 (Many)
To Column Id: 2084
To Cardinality: 1 (One)
Cross Filtering: 1 (Single)
Is Active: True
```

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| from_cardinality | [Relationship Cardinalities](#relationship-cardinalities) |
| to_cardinality | [Relationship Cardinalities](#relationship-cardinalities) |
| cross_filtering_behavior | [Relationship Crossfilter Types](#relationship-crossfilter-types) |
| from_column_id | [Columns](#columns) |
| to_column_id | [Columns](#columns) |

## Reports
Summary: Each record in this table references a single PBIX report.

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| report_id | [Annotations](#annotations) |
| report_id | [Data Sources](#data-sources) |
| report_id | [Expressions](#expressions) |
| report_id | [Linguistic Metadata](#linguistic-metadata) |
| report_id | [tables](#tables) |
| report_id | [Pages](#pages) |

## Tables

Summary: Very little useful in the table itself, except for the name. Useful information about tables is in the [Partitions](#partitions) table.

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| table_id | [Columns](#columns) |
| table_id | [Hierarchies](#hierarchies) |
| table_id | [Measures](#measures) |
| table_id | [Partitions](#measures) |

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#Reports) |

## Visuals

Summary: contains information about each visualization (including slicers, etc) in a report. Contains information on what type (Bar Chart, Text Box, Slicer) of visual, the positioning, and whether drilling filters other visuals. The `raw` field can contain information about how the data is queried to generate the visual

### Examples

```
{"x": 328.0, "y": 72.0, "z": 10250.0, "id": 6495302, "query": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"s\",\"Entity\":\"Sales\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Category\"},\"Name\":\"Sales.Category\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"SalesAmount\"}},\"Function\":0},\"Name\":\"Sum(Sales.SalesAmount)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"NSAT\"}},\"Function\":1},\"Name\":\"Sum(Sales.NSAT)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"RePurch\"}},\"Function\":1},\"Name\":\"Sum(Sales.RePurch)\"}],\"Where\":[{\"Condition\":{\"And\":{\"Left\":{\"Comparison\":{\"ComparisonKind\":2,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"NSAT\"}},\"Right\":{\"Literal\":{\"Value\":\"2D\"}}}},\"Right\":{\"Comparison\":{\"ComparisonKind\":4,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"NSAT\"}},\"Right\":{\"Literal\":{\"Value\":\"5D\"}}}}}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"SalesAmount\"}},\"Function\":0}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":1000}}},\"Version\":1}}}]}", "width": 440.0, "config": {"name": "4e9883262660200aa95e", "layouts": [{"id": 0, "position": {"x": 328, "y": 72, "z": 10250, "width": 440, "height": 568}}], "singleVisual": {"title": {"show": true, "text": "Sales for Top 5 Categories", "fontSize": "15", "alignment": "center", "fontColor": "#666666"}, "objects": {"labels": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "fontSize": {"expr": {"Literal": {"Value": "'8'"}}}, "labelPosition": {"expr": {"Literal": {"Value": "'InsideBase'"}}}, "backgroundColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}, "enableBackground": {"expr": {"Literal": {"Value": "true"}}}, "labelOrientation": {"expr": {"Literal": {"Value": "0D"}}}, "backgroundTransparency": {"expr": {"Literal": {"Value": "'68'"}}}}}], "legend": [{"properties": {"legendMarkerRendering": {"expr": {"Literal": {"Value": "'lineOnly'"}}}}}], "dataPoint": [{"properties": {"fillRule": {"linearGradient2": {"max": {"color": {"expr": {"Literal": {"Value": "'#666666'"}}}}, "min": {"color": {"expr": {"Literal": {"Value": "'#cccccc'"}}}}, "nullColoringStrategy": {"strategy": {"expr": {"Literal": {"Value": "'asZero'"}}}}}}, "defaultCategoryColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F9A030'"}}}}}}}, {"selector": {"metadata": "Sum(Sales.NSAT)"}, "properties": {"fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#EF443A'"}}}}}}}, {"selector": {"metadata": "Sum(Sales.RePurch)"}, "properties": {"fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#892577'"}}}}}}}], "valueAxis": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "secEnd": {"expr": {"Literal": {"Value": "7D"}}}, "secStart": {"expr": {"Literal": {"Value": "0D"}}}, "alignZeros": {"expr": {"Literal": {"Value": "false"}}}, "gridlineShow": {"expr": {"Literal": {"Value": "true"}}}}}], "lineStyles": [{"properties": {"lineStyle": {"expr": {"Literal": {"Value": "'dashed'"}}}, "showSeries": {"expr": {"Literal": {"Value": "true"}}}, "strokeWidth": {"expr": {"Literal": {"Value": "3D"}}}}}, {"selector": {"metadata": "Sum(Sales.RePurch)"}, "properties": {"lineStyle": {"expr": {"Literal": {"Value": "'dotted'"}}}}}]}, "background": {"show": true, "transparency": "60"}, "visualType": "lineStackedColumnComboChart", "projections": {"Y": [{"queryRef": "Sum(Sales.SalesAmount)"}], "Y2": [{"queryRef": "Sum(Sales.NSAT)"}, {"queryRef": "Sum(Sales.RePurch)"}], "Category": [{"active": true, "queryRef": "Sales.Category"}]}, "prototypeQuery": {"From": [{"Name": "s", "Entity": "Sales"}], "Select": [{"Name": "Sales.Category", "Column": {"Property": "Category", "Expression": {"SourceRef": {"Source": "s"}}}}, {"Name": "Sum(Sales.SalesAmount)", "Aggregation": {"Function": 0, "Expression": {"Column": {"Property": "SalesAmount", "Expression": {"SourceRef": {"Source": "s"}}}}}}, {"Name": "Sum(Sales.NSAT)", "Aggregation": {"Function": 1, "Expression": {"Column": {"Property": "NSAT", "Expression": {"SourceRef": {"Source": "s"}}}}}}, {"Name": "Sum(Sales.RePurch)", "Aggregation": {"Function": 1, "Expression": {"Column": {"Property": "RePurch", "Expression": {"SourceRef": {"Source": "s"}}}}}}], "OrderBy": [{"Direction": 2, "Expression": {"Aggregation": {"Function": 0, "Expression": {"Column": {"Property": "SalesAmount", "Expression": {"SourceRef": {"Source": "s"}}}}}}}], "Version": 2}, "columnProperties": {"Sum(Sales.NSAT)": {"displayName": "Avg. Net Satisfaction"}, "Sum(Sales.RePurch)": {"displayName": "Avg. Likelihood to Purchase Again"}, "Sum(Sales.SalesAmount)": {"displayName": "Sales Amount"}}, "drillFilterOtherVisuals": true}}, "height": 568.0, "filters": "[]", "queryHash": -8661283248748414215, "dataTransforms": "{\"objects\":{\"dataPoint\":[{\"properties\":{\"defaultCategoryColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#F9A030'\"}}}}},\"fillRule\":{\"linearGradient2\":{\"min\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#cccccc'\"}}}},\"max\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#666666'\"}}}},\"nullColoringStrategy\":{\"strategy\":{\"expr\":{\"Literal\":{\"Value\":\"'asZero'\"}}}}}}}},{\"properties\":{\"fill\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#EF443A'\"}}}}}},\"selector\":{\"metadata\":\"Sum(Sales.NSAT)\"}},{\"properties\":{\"fill\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#892577'\"}}}}}},\"selector\":{\"metadata\":\"Sum(Sales.RePurch)\"}}],\"labels\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"labelPosition\":{\"expr\":{\"Literal\":{\"Value\":\"'InsideBase'\"}}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"'8'\"}}},\"labelOrientation\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}},\"enableBackground\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"backgroundColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#FFFFFF'\"}}}}},\"backgroundTransparency\":{\"expr\":{\"Literal\":{\"Value\":\"'68'\"}}}}}],\"valueAxis\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"alignZeros\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}},\"secEnd\":{\"expr\":{\"Literal\":{\"Value\":\"7D\"}}},\"secStart\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}},\"gridlineShow\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}}}}],\"lineStyles\":[{\"properties\":{\"lineStyle\":{\"expr\":{\"Literal\":{\"Value\":\"'dashed'\"}}},\"showSeries\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"strokeWidth\":{\"expr\":{\"Literal\":{\"Value\":\"3D\"}}}}},{\"properties\":{\"lineStyle\":{\"expr\":{\"Literal\":{\"Value\":\"'dotted'\"}}}},\"selector\":{\"metadata\":\"Sum(Sales.RePurch)\"}}],\"legend\":[{\"properties\":{\"legendMarkerRendering\":{\"expr\":{\"Literal\":{\"Value\":\"'lineOnly'\"}}}}}]},\"projectionOrdering\":{\"Category\":[0],\"Y\":[1],\"Y2\":[2,3]},\"projectionActiveItems\":{\"Category\":[{\"queryRef\":\"Sales.Category\",\"suppressConcat\":false}]},\"splits\":[{\"selects\":{\"0\":true,\"1\":true}},{\"selects\":{\"0\":true,\"2\":true,\"3\":true}}],\"queryMetadata\":{\"Select\":[{\"Restatement\":\"Category\",\"Name\":\"Sales.Category\",\"Type\":2048},{\"Restatement\":\"Sales Amount\",\"Name\":\"Sum(Sales.SalesAmount)\",\"Type\":1,\"Format\":\"\\\\$#,0.00;(\\\\$#,0.00);\\\\$#,0.00\"},{\"Restatement\":\"Avg. Net Satisfaction\",\"Name\":\"Sum(Sales.NSAT)\",\"Type\":1,\"Format\":\"0.00\"},{\"Restatement\":\"Avg. Likelihood to Purchase Again\",\"Name\":\"Sum(Sales.RePurch)\",\"Type\":1,\"Format\":\"0.00\"}]},\"visualElements\":[{\"DataRoles\":[{\"Name\":\"Category\",\"Projection\":0,\"isActive\":true},{\"Name\":\"Y\",\"Projection\":1,\"isActive\":false}]},{\"DataRoles\":[{\"Name\":\"Category\",\"Projection\":0,\"isActive\":true},{\"Name\":\"Y2\",\"Projection\":2,\"isActive\":false},{\"Name\":\"Y2\",\"Projection\":3,\"isActive\":false}]}],\"selects\":[{\"displayName\":\"Category\",\"queryName\":\"Sales.Category\",\"roles\":{\"Category\":true},\"type\":{\"category\":null,\"underlyingType\":1},\"expr\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Sales\"}},\"Property\":\"Category\"}}},{\"displayName\":\"Sales Amount\",\"format\":\"\\\\$#,0.00;(\\\\$#,0.00);\\\\$#,0.00\",\"queryName\":\"Sum(Sales.SalesAmount)\",\"roles\":{\"Y\":true},\"sort\":2,\"sortOrder\":0,\"type\":{\"category\":null,\"underlyingType\":259},\"expr\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Sales\"}},\"Property\":\"SalesAmount\"}},\"Function\":0}}},{\"displayName\":\"Avg. Net Satisfaction\",\"format\":\"0.00\",\"queryName\":\"Sum(Sales.NSAT)\",\"roles\":{\"Y2\":true},\"type\":{\"category\":null,\"underlyingType\":259},\"expr\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Sales\"}},\"Property\":\"NSAT\"}},\"Function\":1}}},{\"displayName\":\"Avg. Likelihood to Purchase Again\",\"format\":\"0.00\",\"queryName\":\"Sum(Sales.RePurch)\",\"roles\":{\"Y2\":true},\"type\":{\"category\":null,\"underlyingType\":259},\"expr\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Sales\"}},\"Property\":\"RePurch\"}},\"Function\":1}}}]}"}
```

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| page_id | [Pages](#pages) |

## Static Fields

## Annotation Object Types

Summary: Lists the pbi_ids of each object ([measures](#measures), [columns](#columns), [expressions](#expressions), etc.) and the name of the object.

### Sample

```
id,pbi_id,name
1,1,report
2,3,table
```

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| object_type | [Annotations](#annotations) |

## Datatypes

Summary: Lists the pbi_ids of each type of data and the name. Currently pbi_id=19 has not been deciphered.

### Sample

```
id,pbi_id,name
1,1,Text
2,2,Text
3,6,Whole Number
```

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| data_type | [Measures](#measures) |
| data_type | [Columns](#columns) |

## Relationship Cardinalities

Summary: A table with the options `One` and `Many`.

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| from_cardinality | [Relationships](#relationships) |
| to_cardinality | [Relationships](#relationships) |

## Relationship Crossfilter Types

Summary: A table with the options `Single` and `Both`.

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| cross_filtering_behavior | [Relationships](#relationships) |

## Views

# Example


# Facts

Slicers work by using the same drill on filter as other visuals

# Developers
AttributeHierarchy has not been deciphered