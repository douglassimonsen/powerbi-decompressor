# Schema

Visuals depend on measures or columns (possibly calculated)
Measures and columns depend on tables
Tables (generally) depend on outside datasources

## Parsed Fields

### Annotations

Summary: Annotations are notes 

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |
| object_type | [Annotation Object Types](#annotation-object-types) |

### Columns

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| table_id | [Tables](#tables) |
| data_type | [Datatypes](#datatypes) |

Foreign Keys From: 

| Column | Table |
| ------ | ----- |
| column_id | Levels |
| hierarchy_column_id | Levels |

### Data Sources

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |

Foreign Keys From: 

| Column | Table |
| ------ | ----- |
| column_id | Levels |
| table_id | Partitions |


### Expressions

Foreign Keys To:

| Column | Table |
| ------ | ----- |
| report_id | [Reports](#reports) |

### Hierarchies

### Levels

### Linguistic Metadata

### Measures

### Pages

### Partitions

### Relationships

### Reports
Summary: Each record in this table references a single PBIX report.

Foreign Keys From:

| Column | Table |
| ------ | ----- |
| report_id | [Annotations](#annotations) |
| report_id | [Data Sources](#data-sources) |
| report_id | [Expressions](#expressions) |
| report_id | [Linguistic Metadata](#linguistic-metadata) |
| report_id | [Relationships](#relationships) |
| report_id | [tables](#tables) |
| report_id | [Pages](#pages) |

### Tables

### Visuals

## Static Fields

### Annotation Object Types

### Datatypes

### Relationship Cardinalities

### Relationship Crossfilter Types

## Views

# Example


# Facts

Slicers work by using the same drill on filter as other visuals

# Developers
AttributeHierarchy has not been deciphered