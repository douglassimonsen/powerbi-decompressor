import os, pathlib
import util
import structlog
import json

logger = structlog.getLogger()
insert_queries = {}
for f in os.listdir(pathlib.Path(__file__).parent / "queries"):
    insert_queries[f[:-4]] = open(pathlib.Path(__file__).parent / "queries" / f).read()


def gen_query(table_name, data, returning=("pbi_id", "id")):
    if len(data[table_name]) == 0:
        return None
    columns = data[table_name][0].keys()
    cols = ", ".join(columns)
    vals = ", ".join(f"%({x})s" for x in columns)
    ret = f"""
    insert into pbi.{table_name} ({cols})
    values ({vals})
    """
    if returning is not None:
        ret += "returning " + ", ".join(returning)
    return ret


def main(data, static_tables):
    def fix_annotation():
        cursor.execute("select pbi_id, name from pbi.annotation_object_types")
        object_types = dict(cursor.fetchall())
        for row in data["annotations"]:
            object_name = object_types[row["object_type"]]
            if object_name == "hierarchy":
                object_name = "hierarchies"
            else:
                object_name += "s"

            if object_name == "query_groups":
                logger.warn("Missing Table", table="query_groups")
                row["object_id"] = None
            elif object_name != "reports":
                row["object_id"] = gen_ids[object_name][row["object_id"]]
            else:
                row["object_id"] = gen_ids[object_name][None]

    def get_ids(dependency):
        dependency["parent_id"] = gen_ids[dependency["parent_type"] + "s"][
            dependency["parent_pbi_id"]
        ]
        dependency["child_id"] = gen_ids[dependency["child_type"] + "s"][
            dependency["child_pbi_id"]
        ]

    def run_table(
        table_name,
        returning=("pbi_id", "id"),
        remove=tuple(),
        add=tuple(),
    ):
        for row in data[table_name]:  # must add columns before generating query
            for chg in add:
                old_val = row.get(
                    chg.get("from_col", chg["to"])
                )  # we use get to default to None for the reports
                if chg.get("skip_nulls") and old_val is None:
                    continue
                try:
                    row[chg["to"]] = gen_ids[chg["from_table"]][old_val]
                except:
                    raise ValueError(
                        f'ID {old_val} was not found in table {chg["from_table"]}'
                    )
            for col in remove:
                del row[col]

        insert_query = gen_query(table_name, data, returning=returning)
        for row in data[table_name]:
            cursor.execute(insert_query, row)
            ret = cursor.fetchone()
            gen_ids.setdefault(table_name, {})[ret[0]] = ret[1]

    gen_ids = {**static_tables}  # needed to avoid passing
    logger.info("loading_to_postgres")
    with util.get_conn() as conn:
        conn.set_session(autocommit=False)
        cursor = conn.cursor()
        run_table("reports", remove=("filters",), returning=("pbi_id", "id"))
        gen_ids["reports"][None] = list(gen_ids["reports"].values())[0]
        run_table(
            "pages",
            remove=("filters", "pbi_id"),
            returning=("ordinal", "id"),
            add=[{"to": "report_id", "from_table": "reports"}],
        )
        run_table(
            "visuals",
            remove=("page_ordinal", "filters", "selects"),
            add=[{"to": "page_id", "from_table": "pages", "from_col": "page_ordinal"}],
        )
        run_table(
            "linguistic_metadata",
            add=[{"to": "report_id", "from_table": "reports"}],
        )
        run_table(
            "data_sources",
            add=[{"to": "report_id", "from_table": "reports"}],
        )
        run_table(
            "expressions",
            add=[{"to": "report_id", "from_table": "reports"}],
        )
        run_table(
            "tables",
            add=[
                {"to": "report_id", "from_table": "reports"},
            ],
        )
        run_table(
            "hierarchies",
            add=[{"to": "table_id", "from_table": "tables"}],
        )
        run_table(
            "partitions",
            add=[
                {"to": "table_id", "from_table": "tables"},
                {
                    "to": "data_source_id",
                    "from_table": "data_sources",
                    "skip_nulls": True,
                },
            ],
        )
        run_table(
            "columns",
            add=[
                {"to": "data_type", "from_table": "datatypes"},
                {"to": "table_id", "from_table": "tables"},
            ],
        )
        run_table(
            "levels",
            add=[
                {"to": "hierarchy_id", "from_table": "hierarchies"},
                {"to": "column_id", "from_table": "columns"},
                {
                    "to": "hierarchy_column_id",
                    "from_table": "columns",
                    "skip_nulls": True,
                },
            ],
        )
        run_table(
            "relationships",
            add=[
                {"to": "report_id", "from_table": "reports"},
                {"to": "from_column_id", "from_table": "columns"},
                {"to": "to_column_id", "from_table": "columns"},
                {"to": "from_cardinality", "from_table": "relationship_cardinalities"},
                {"to": "to_cardinality", "from_table": "relationship_cardinalities"},
                {
                    "to": "cross_filtering_behavior",
                    "from_table": "relationship_crossfilter_types",
                },
            ],
        )
        run_table(
            "measures",
            add=[
                {"to": "table_id", "from_table": "tables"},
                {"to": "data_type", "from_table": "datatypes"},
            ],
        )
        fix_annotation()
        run_table(
            "annotations",
            add=[
                {"to": "report_id", "from_table": "reports"},
                {"to": "object_type", "from_table": "annotation_object_types"},
            ],
        )

        for dependency in data["dax_dependencies"]:
            get_ids(dependency)
            cursor.execute(insert_queries["dax_dependencies"], dependency)
        conn.commit()


if __name__ == "__main__":
    main()
