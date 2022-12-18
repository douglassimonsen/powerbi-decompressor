import json
from pprint import pprint
import structlog
from extract_library import m_parser
from bs4 import BeautifulSoup

logger = structlog.getLogger()


def get_tables(tables):
    ret = []
    for table in tables:
        ret.append(
            {
                "pbi_id": str(table["ID"]),
                "name": table["Name"],
                "raw": json.dumps(table),
            }
        )
    return ret


def get_measures(measures):
    ret = []
    for measure in measures:
        if "Expression" not in measure:
            logger.warn(
                "measure_parse_issue", measure=measure
            )  # in the cases I found, these also freaked out PBI, so I think it's OK to ignore. In PBI, it was shown without a definition and deleted itself if you moved to a different measure
        ret.append(
            {
                "pbi_id": str(measure["ID"]),
                "name": measure["Name"],
                "table_id": str(measure["TableID"]),
                "expression": measure.get("Expression"),
                "data_type": str(measure["DataType"]),
                "raw": json.dumps(measure),
            }
        )
    return ret


def get_table_columns(columns):
    ret = []
    for column in columns:
        ret.append(
            {
                "pbi_id": str(column["ID"]),
                "table_id": str(column["TableID"]),
                "data_type": str(column["ExplicitDataType"]),
                "name": column.get("ExplicitName", column.get("InferredName")),
                "is_hidden": column.get("isHidden", False),
                "expression": column.get("Expression"),
                "raw": json.dumps(column),
            }
        )
    return ret


def get_partitions(partitions):
    ret = []
    for partition in partitions:
        source_details = m_parser.get_sources(partition["QueryDefinition"])
        source_type = None
        if len(source_details) >= 1:
            source_type = source_details[0].get("type")
        ret.append(
            {
                "pbi_id": str(partition["ID"]),
                "name": partition["Name"],
                "query_definition": partition["QueryDefinition"],
                "table_id": str(partition["TableID"]),
                "data_source_id": str(partition["DataSourceID"])
                if "DataSourceID" in partition
                else None,
                "source_type": source_type,
                "source_details": json.dumps(source_details[0])
                if source_details
                else None,
                "raw": json.dumps(partition),
            }
        )
    return ret


def get_dataconnections(connections):
    return [
        {
            "pbi_id": conn["ID"],
            "name": conn["Name"],
            "type": conn["Type"],
            "max_connections": conn["MaxConnections"],
            "modified_time": conn["ModifiedTime"],
            "connection_string": conn["ConnectionString"],
            "impersonation_mode": conn["ImpersonationMode"],
            "timeout": conn["Timeout"],
            "raw": json.dumps(conn),
        }
        for conn in connections
    ]


def get_expressions(expressions):
    return [
        {
            "pbi_id": expr["ID"],
            "name": expr["Name"],
            "kind": expr["Kind"],
            "modified_time": expr["ModifiedTime"],
            "expression": expr["Expression"],
            "raw": json.dumps(expr),
        }
        for expr in expressions
    ]


def get_linguistic_metadata(lms):
    def parse_xml(content):
        data = BeautifulSoup(lm["Content"], "xml")
        schema = data.find("LinguisticSchema").attrs
        entities = [
            {
                "conceptual_entity": row.attrs.get("ConceptualEntity"),
                "name": row.get("Name"),
                "source": row.get("Source"),
                "words": [x.text for x in row.find_all("Word")],
            }
            for row in data.find_all("Entity")
        ]
        return {
            "version": "1.0.0",  # 2.0.0 is JSON
            "pbi_id": lm["ID"],
            "culture_id": lm["CultureID"],
            "language": schema.get("Language"),
            "dynamic_improvement": schema.get("DynamicImprovement"),
            "entities": json.dumps(entities),
            "relationships": None,
            "examples": None,
            "modified_time": lm["ModifiedTime"],
        }

    def parse_json(content):
        return {
            "version": content["Version"],
            "pbi_id": None,
            "culture_id": None,
            "language": content["Language"],
            "dynamic_improvement": content["DynamicImprovement"],
            "entities": json.dumps(content["Entities"])
            if "Entities" in content
            else None,
            "relationships": json.dumps(content["Relationships"])
            if "Relationships" in content
            else None,
            "examples": json.dumps(content["Examples"])
            if "Examples" in content
            else None,
            "modified_time": None,
        }

    ret = []
    for lm in lms:
        if isinstance(lm["Content"], str):
            ret.append(parse_xml(lm["Content"]))
        elif isinstance(lm["Content"], dict):
            ret.append(parse_json(lm["Content"]))
        else:
            TypeError(lm["Content"])
    return ret


def get_annotations(annotations):
    for annotation in annotations:
        if (
            "Value" not in annotation
        ):  # yeah there are some records that just don't have a value ({'ID': 12869, 'ObjectID': 12, 'ObjectType': 3, 'Name': 'PBI_DescriptionAtRefresh', 'ModifiedTime': '2020-11-10T21:52:23.696667'})
            annotation["Value"] = None
        elif isinstance(annotation["Value"], (list, dict)):
            annotation["Value"] = json.dumps(annotation["Value"], indent=2)
    return [
        {
            "pbi_id": annotation["ID"],
            "object_type": str(annotation["ObjectType"]),
            "name": annotation["Name"],
            "value": annotation["Value"],
            "modified_time": annotation["ModifiedTime"],
            "object_id": str(annotation["ObjectID"]),
        }
        for annotation in annotations
    ]


def get_relationships(relationships):
    return [
        {
            "from_column_id": str(relationship["FromColumnID"]),
            "from_cardinality": str(relationship["FromCardinality"]),
            "to_column_id": str(relationship["ToColumnID"]),
            "to_cardinality": str(relationship["ToCardinality"]),
            "cross_filtering_behavior": str(relationship["CrossFilteringBehavior"]),
            "is_active": relationship["IsActive"],
            "pbi_id": relationship["ID"],
            "name": relationship["Name"],
            "modified_time": relationship["ModifiedTime"],
            "refreshed_time": relationship["RefreshedTime"],
            "raw": json.dumps(relationship),
        }
        for relationship in relationships
    ]


def get_hierarchies(hierarchies):
    return [
        {
            "pbi_id": hierarchy["ID"],
            "table_id": str(hierarchy["TableID"]),
            "name": hierarchy["Name"],
            "is_hidden": hierarchy["IsHidden"],
            "state": hierarchy["State"],
            "modified_time": hierarchy["ModifiedTime"],
            "structure_modified_time": hierarchy["StructureModifiedTime"],
            "refreshed_time": hierarchy["RefreshedTime"],
            "hide_members": hierarchy["HideMembers"],
        }
        for hierarchy in hierarchies
    ]


def get_levels(levels, variations):
    hierarchy_column = {v["DefaultHierarchyID"]: v["ColumnID"] for v in variations}
    return [
        {
            "pbi_id": str(level["ID"]),
            "hierarchy_id": str(level["HierarchyID"]),
            "ordinal": level["Ordinal"],
            "name": level["Name"],
            "column_id": str(level["ColumnID"]),
            "hierarchy_column_id": str(hierarchy_column[level["HierarchyID"]])
            if level["HierarchyID"] in hierarchy_column
            else None,
            "modified_time": level["ModifiedTime"],
        }
        for level in levels
    ]


def main(data):
    hierarchies = get_hierarchies(data["Hierarchy"])
    levels = get_levels(data["Level"], data["Variation"])
    annotations = get_annotations(data["Annotation"])
    data_sources = get_dataconnections(data["DataSource"])
    partitions = get_partitions(data["Partition"])
    tables = get_tables(data["Table"])
    measures = get_measures(data["Measure"])
    columns = get_table_columns(data["Column"])
    expressions = get_expressions(data["Expression"])
    relationships = get_relationships(data["Relationship"])
    linguistic_metadata = get_linguistic_metadata(data["LinguisticMetadata"])
    return {
        "tables": tables,
        "annotations": annotations,
        "partitions": partitions,
        "data_sources": data_sources,
        "expressions": expressions,
        "measures": measures,
        "columns": columns,
        "linguistic_metadata": linguistic_metadata,
        "relationships": relationships,
        "hierarchies": hierarchies,
        "levels": levels,
    }


if __name__ == "__main__":
    with open("test.json") as f:
        data = json.load(f)["data_model"]
    main(data)
