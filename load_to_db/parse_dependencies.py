import extract_library
import extract_library.dax_parser
from pprint import pprint
import structlog
from frozendict import frozendict

logger = structlog.getLogger()


def get_parents(expr, child_id, child_type, parents, column_table):
    if not isinstance(expr, str):  # some exprs are just a number, like 10
        return []

    ret = []
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


def main(data):
    table_dict = {t["pbi_id"]: t["name"] for t in data["tables"]}
    parents = {
        (table_dict[m["TableID"]], m["name"], None): {
            "parent_pbi_id": m["pbi_id"],
            "parent_type": "column",
        }
        for m in data["measures"] + data["columns"]
    }

    column_table = {}
    for (tab, col, _) in parents.keys():
        column_table.setdefault(col, []).append(tab)
    column_table = {k: v[0] for k, v in column_table.items() if len(v) == 1}

    dependencies = []
    for field in ["columns", "measures"]:
        for row in data[field]:
            if row["Expression"] is None:
                continue
            dependencies.extend(
                get_parents(
                    row["Expression"], row["pbi_id"], field[:-1], parents, column_table
                )
            )

    table_dict = {x["pbi_id"]: x["name"] for x in data["tables"]}
    parents = {
        (table_dict[x["TableID"]], x["name"]): {
            "parent_pbi_id": x["pbi_id"],
            "parent_type": c[:-1],
        }
        for c in ["measures", "columns"]
        for x in data[c]
    }
    for visual in data["visuals"]:
        for c in ["selects", "filters"]:
            for ds in visual[c]:
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
                            "depdency_type": f"visual_{c[:-1]}",
                            **parents[(ds_name, ds_column_name)],
                        }
                    )
                )
    return [dict(x) for x in set(map(lambda x: frozendict(x), dependencies))]
