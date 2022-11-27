import parse_datasources
import parse_visuals
import json
import zipfile
import extract_library
import extract_library.dax_parser
from pprint import pprint
import structlog
from frozendict import frozendict

logger = structlog.getLogger()


def extract_data(source):
    ret = {}
    with zipfile.ZipFile(source) as zf:
        ret["layout"] = json.loads(
            zf.open("Report/Layout", "r").read().decode("utf-16-le")
        )
    pbi = extract_library.PowerBi(source)
    ret["data_model"] = pbi.read_schema()
    return ret


def discover_dependencies(data):
    def get_parents(expr, child_id, child_type):
        """
        TODO: fix with lark
        """
        ret = []
        if not isinstance(expr, str):  # some exprs are just a number, like 10
            return ret

        for var in extract_library.dax_parser.get_variables(expr):
            if (
                var[0] is None and var[1] in column_table
            ):  # temporary since hierarchy has some issues
                var = (column_table[var[1]], var[1], var[2])
            if var in parents:
                ret.append(
                    {
                        **parents[var],
                        "child_pbi_id": child_id,
                        "child_type": child_type,
                    }
                )
        return ret

    dependencies = []
    table_dict = {t["pbi_id"]: t["name"] for t in data["tables"]}
    measures = {
        (table_dict[m["TableID"]], m["name"], None): {
            "parent_pbi_id": m["pbi_id"],
            "parent_type": "measure",
        }
        for m in data["measures"]
    }
    columns = {
        (table_dict[m["TableID"]], m["name"], None): {
            "parent_pbi_id": m["pbi_id"],
            "parent_type": "column",
        }
        for m in data["columns"]
    }
    parents = {**columns, **measures}

    column_table = {}
    for (tab, col, _) in parents.keys():
        column_table.setdefault(col, []).append(tab)
    column_table = {k: v[0] for k, v in column_table.items() if len(v) == 1}

    for column in data["columns"]:
        if column["Expression"] is None:
            continue
        dependencies.extend(
            get_parents(column["Expression"], column["pbi_id"], "column")
        )

    for column in data["measures"]:
        dependencies.extend(
            get_parents(column["Expression"], column["pbi_id"], "measure")
        )

    table_dict = {x["pbi_id"]: x["name"] for x in data["tables"]}
    parents = {
        **{
            (table_dict[x["TableID"]], x["name"]): {
                "parent_pbi_id": x["pbi_id"],
                "parent_type": "measure",
            }
            for x in data["measures"]
        },
        **{
            (table_dict[x["TableID"]], x["name"]): {
                "parent_pbi_id": x["pbi_id"],
                "parent_type": "column",
            }
            for x in data["columns"]
        },
    }
    for visual in data["visuals"]:
        for ds in visual["selects"]:
            if (
                ds is None
                or "Property" not in ds
                or "Entity" not in ds["Expression"]["SourceRef"]
            ):
                logger.info(
                    "visual select parse issue", expr=ds, name=visual["pbi_id"]
                )  # there are elements that aren't connected to any table
                continue
            ds_name = ds["Expression"]["SourceRef"]["Entity"]
            ds_column_name = ds["Property"]
            if (ds_name, ds_column_name) not in parents:
                logger.info(
                    "missing_dependency", tbl_name=ds_name, col_name=ds_column_name
                )  # in the two cases I checked, this occurred when the field was removed from the source after it was added to the visual
                continue
            dependencies.append(
                frozendict(
                    {
                        "child_pbi_id": visual["pbi_id"],
                        "child_type": "visual",
                        "depdency_type": "visual_select",
                        **parents[(ds_name, ds_column_name)],
                    }
                )
            )
        for ds in visual["filters"]:
            if (
                ds is None
                or "Property" not in ds
                or "Entity" not in ds["Expression"]["SourceRef"]
            ):
                logger.info("visual filter parse issue", expr=ds, name=visual["pbi_id"])
                continue
            ds_name = ds["Expression"]["SourceRef"]["Entity"]
            ds_column_name = ds["Property"]
            if (ds_name, ds_column_name) not in parents:
                logger.info(
                    "missing_dependency",
                    tbl_name=ds_name,
                    col_name=ds_column_name,
                    visual=visual["pbi_id"],
                )  # in the two cases I checked, this occurred when the field was removed from the source after it was added to the visual
                continue
            dependencies.append(
                {
                    "child_pbi_id": visual["pbi_id"],
                    "child_type": "visual",
                    "depdency_type": "visual_filter",
                    **parents[(ds_name, ds_column_name)],
                }
            )
    return [dict(x) for x in set(map(lambda x: frozendict(x), dependencies))]


def main(source):
    raw_data = extract_data(source)
    with open("test.json", "w") as f:
        json.dump(raw_data, f, indent=4)

    data = parse_datasources.main(raw_data["data_model"])
    data = {
        **data,
        **parse_visuals.main(raw_data["layout"]),
        "reports": [
            {
                "file_path": source,
                "created_dt": raw_data["data_model"]["Model"][0]["ModifiedTime"],
            }
        ],
    }
    data["dax_dependencies"] = discover_dependencies(data)
    return data


if __name__ == "__main__":
    main("")
