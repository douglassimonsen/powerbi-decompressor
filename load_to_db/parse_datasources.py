import json
from pprint import pprint
import structlog
from extract_library import m_parser

logger = structlog.getLogger()


def get_tables(tables, datasources):
    datasource_dict = {x["TableID"]: x["pbi_id"] for x in datasources}
    ret = []
    for table in tables:
        ret.append(
            {
                "pbi_id": str(table["ID"]),
                "name": table["Name"],
                "datasourceID": datasource_dict[table["ID"]],
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
            continue
        ret.append(
            {
                "pbi_id": str(measure["ID"]),
                "name": measure["Name"],
                "TableID": str(measure["TableID"]),
                "Expression": measure["Expression"],
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
                "TableID": str(column["TableID"]),
                "data_type": str(column["ExplicitDataType"]),
                "name": column.get("ExplicitName", column.get("InferredName")),
                "isHidden": column.get("isHidden", False),
                "Expression": column.get("Expression"),
                "raw": json.dumps(column),
            }
        )
    return ret


def get_datasources(datasources):
    ret = []
    for datasource in datasources:
        source_details = m_parser.get_sources(datasource["QueryDefinition"])
        source_type = None
        if len(source_details) >= 1:
            source_type = source_details[0].get("type")
        ret.append(
            {
                "pbi_id": str(datasource["ID"]),
                "name": datasource["Name"],
                "QueryDefinition": datasource["QueryDefinition"],
                "TableID": datasource["TableID"],
                "source_type": source_type,
                "source_details": json.dumps(source_details[0])
                if source_details
                else None,
                "raw": json.dumps(datasource),
            }
        )
    return ret


def get_dataconnections(connections):
    return [
        {
            "pbi_id": conn["ID"],
            "Name": conn["Name"],
            "Type": conn["Type"],
            "MaxConnections": conn["MaxConnections"],
            "ModifiedTime": conn["ModifiedTime"],
            "ConnectionString": conn["ConnectionString"],
            "ImpersonationMode": conn["ImpersonationMode"],
            "Timeout": conn["Timeout"],
            "raw": json.dumps(conn),
        }
        for conn in connections
    ]


def main(data):
    datasources = get_datasources(data["Partition"])
    data_connections = get_dataconnections(data["DataSource"])
    tables = get_tables(data["Table"], datasources)
    measures = get_measures(data["Measure"])
    columns = get_table_columns(data["Column"])
    return {
        "tables": tables,
        "datasources": datasources,
        "data_connections": data_connections,
        "measures": measures,
        "columns": columns,
    }


if __name__ == "__main__":
    with open("test.json") as f:
        data = json.load(f)["data_model"]
    main(data)
