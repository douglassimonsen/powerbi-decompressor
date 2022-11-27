import os, pathlib
import util
import structlog

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


def run_table(
    table_name,
    data,
    gen_ids,
    cursor,
    returning=("pbi_id", "id"),
    remove=tuple(),
    add=tuple(),
):
    for row in data[table_name]:  # must add columns before generating query
        for chg in add:
            row[chg["to"]] = gen_ids[chg["from_table"]][
                row[chg.get("from_col", chg["to"])]
            ]
        for col in remove:
            del row[col]

    insert_query = gen_query(table_name, data, returning=returning)
    for row in data[table_name]:
        cursor.execute(insert_query, row)
        ret = cursor.fetchone()
        gen_ids[table_name][ret[0]] = ret[1]


def main(data, static_tables):
    def get_ids(dependency):
        dependency["parent_id"] = gen_ids[dependency["parent_type"] + "s"][
            dependency["parent_pbi_id"]
        ]
        dependency["child_id"] = gen_ids[dependency["child_type"] + "s"][
            dependency["child_pbi_id"]
        ]

    gen_ids = {
        "report": None,
        "pages": {},
        "tables": {},
        "columns": {},
        "measures": {},
        "visuals": {},
        "datasources": {},
        "datasource_columns": {},
        **static_tables,
    }
    logger.info("loading_to_postgres")
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_queries["reports"], data["report"])
        gen_ids["report_id"] = cursor.fetchone()[0]
        for page in data["pages"]:
            page["report_id"] = gen_ids["report_id"]
        for table in data["tables"]:
            table["report_id"] = gen_ids["report_id"]
        for datasource in data["datasources"]:
            datasource["report_id"] = gen_ids["report_id"]

        run_table("pages", data, gen_ids, cursor, returning=("ordinal", "id"))
        run_table(
            "visuals",
            data,
            gen_ids,
            cursor,
            remove=("page_ordinal", "filters", "selects"),
            add=[{"to": "page_id", "from_table": "pages", "from_col": "page_ordinal"}],
        )
        run_table("datasources", data, gen_ids, cursor)
        run_table(
            "tables",
            data,
            gen_ids,
            cursor,
            add=[{"to": "datasourceID", "from_table": "datasources"}],
        )
        run_table(
            "columns",
            data,
            gen_ids,
            cursor,
            add=[
                {"to": "data_type", "from_table": "datatypes"},
                {"to": "TableID", "from_table": "tables"},
            ],
        )
        run_table(
            "measures",
            data,
            gen_ids,
            cursor,
            add=[
                {"to": "TableID", "from_table": "tables"},
            ],
        )

        for dependency in data["dax_dependencies"]:
            get_ids(dependency)
            cursor.execute(insert_queries["dax_dependencies"], dependency)
        conn.commit()


if __name__ == "__main__":
    main()
