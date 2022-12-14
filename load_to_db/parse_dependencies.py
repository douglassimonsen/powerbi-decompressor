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
                    "dependency_type": "static",
                }
            )
    return ret


def main(data):
    table_dict = {t["pbi_id"]: t["name"] for t in data["tables"]}
    parents = {
        (table_dict[m["table_id"]], m["name"], None): {
            "parent_pbi_id": m["pbi_id"],
            "parent_type": c[:-1],
        }
        for c in ["measures", "columns"]
        for m in data[c]
    }
    table_dict = {c["pbi_id"]: table_dict[c["table_id"]] for c in data["columns"]}
    column_dict = {c["pbi_id"]: c["name"] for c in data["columns"]}
    parents |= {
        (
            table_dict[l["hierarchy_column_id"]],
            column_dict[l["hierarchy_column_id"]],
            l["name"],
        ): {"parent_pbi_id": l["pbi_id"], "parent_type": "level"}
        for l in data["levels"]
        if l["hierarchy_column_id"] is not None
    }
    column_table = {}
    for (tab, col, _) in parents.keys():
        column_table.setdefault(col, []).append(tab)
    column_table = {k: v[0] for k, v in column_table.items() if len(v) == 1}

    dependencies = []
    for field in ["columns", "measures"]:
        for row in data[field]:
            dependencies.extend(
                get_parents(
                    row["expression"], row["pbi_id"], field[:-1], parents, column_table
                )
            )

    for field in ["visuals", "pages", "reports"]:
        for visual in data[field]:
            for c in ["selects", "filters"]:
                for ds in visual.get(c, []):
                    if (
                        ds is None
                        or "Property" not in ds
                        or "Entity" not in ds["Expression"]["SourceRef"]
                    ):
                        logger.warn(
                            "visual select parse issue", expr=ds, name=visual["pbi_id"]
                        )  # there are elements that aren't connected to any table
                        continue
                    ds_name = ds["Expression"]["SourceRef"]["Entity"]
                    ds_column_name = ds["Property"]
                    ds_level_name = ds.get("Level")
                    if (ds_name, ds_column_name, ds_level_name) not in parents:
                        logger.info(
                            "missing_dependency",
                            tbl_name=ds_name,
                            col_name=ds_column_name,
                        )  # in the two cases I checked, this occurred when the field was removed from the source after it was added to the visual
                        continue
                    dependencies.append(
                        frozendict(
                            {
                                "child_pbi_id": visual["pbi_id"],
                                "child_type": field[:-1],
                                "dependency_type": f"{field[:-1]}_{c[:-1]}",
                                **parents[(ds_name, ds_column_name, ds_level_name)],
                                "dependency_type": "static",
                            }
                        )
                    )
    if data["reports"][0]["filters"]:
        for visual in data["visuals"]:
            dependencies.append(
                {
                    "child_pbi_id": visual["pbi_id"],
                    "child_type": "visual",
                    "dependency_type": "report_visual_filter",
                    "parent_pbi_id": data["reports"][0]["pbi_id"],
                    "parent_type": "report",
                    "dependency_type": "static",
                }
            )
    visual_page_dict = {}
    for visual in data["visuals"]:
        visual_page_dict.setdefault(visual["page_ordinal"], []).append(visual)
    for page in data["pages"]:
        if page["filters"]:
            for visual in visual_page_dict[page["ordinal"]]:
                dependencies.append(
                    {
                        "child_pbi_id": visual["pbi_id"],
                        "child_type": "visual",
                        "dependency_type": "page_visual_filter",
                        "parent_pbi_id": page["pbi_id"],
                        "parent_type": "page",
                        "dependency_type": "static",
                    }
                )
    return [dict(x) for x in set(map(lambda x: frozendict(x), dependencies))]
