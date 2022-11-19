import json
from pprint import pprint
import structlog

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
            }
        )
    return ret


def get_measures(measures):
    ret = []
    for measure in measures:
        if "Expression" not in measure:
            logger.info(
                "measure_parse_issue", measure=measure
            )  # in the cases I found, these also freaked out PBI, so I think it's OK to ignore. In PBI, it was shown without a definition and deleted itself if you moved to a different measure
            continue
        ret.append(
            {
                "pbi_id": str(measure["ID"]),
                "name": measure["Name"],
                "TableID": str(measure["TableID"]),
                "Expression": measure["Expression"],
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
                "data_type": column["ExplicitDataType"],
                "name": column.get("ExplicitName"),
                "isHidden": column.get("isHidden", False),
                "Expression": column.get("Expression"),
            }
        )
    return ret


def get_datasources(datasources):
    ret = []
    for datasource in datasources:
        ret.append(
            {
                "pbi_id": str(datasource["ID"]),
                "name": datasource["Name"],
                "QueryDefinition": datasource["QueryDefinition"],
                "TableID": datasource["TableID"],
            }
        )
    return ret


def main(data):
    datasources = get_datasources(data["Partition"])
    tables = get_tables(data["Table"], datasources)
    measures = get_measures(data["Measure"])
    columns = get_table_columns(data["Column"])
    return {
        "tables": tables,
        "datasources": datasources,
        "measures": measures,
        "columns": columns,
    }


if __name__ == "__main__":
    with open("test.json") as f:
        data = json.load(f)["data_model"]
    main(data)
