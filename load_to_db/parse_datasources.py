import json
from pprint import pprint


def get_datasources(tables):
    ret = []
    for table in tables:
        ret.append(
            {
                "pbi_id": table["ID"],
                "name": table["Name"],
                "parent": None,
                "node_type": "datasource",
            }
        )
    return ret


def get_measures(measures):
    ret = []
    for measure in measures:
        ret.append(
            {
                "pbi_id": measure["ID"],
                "name": measure["Name"],
                "parent": measure["TableID"],
                "expression": measure['Expression'],
                "node_type": "measure",
            }
        )
    return


def get_datasource_columns(columns):
    ret = []
    for column in columns:
        ret.append(
            {
                "pbi_id": column["ID"],
                "datasource_pbi_id": column["TableID"],
                "data_type": column["ExplicitDataType"],
                "name": column.get("ExplicitName"),
                "isHidden": column.get("isHidden", False),
            }
        )
    return ret


def main(data):
    datasources = get_datasources(data["Table"])
    measures = get_measures(data["Measure"])
    columns = get_datasource_columns(data["Column"])
    return {"datasources": datasources, "measures": measures, "columns": columns}


if __name__ == "__main__":
    with open("test.json") as f:
        data = json.load(f)
    main(data)
