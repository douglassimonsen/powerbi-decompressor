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


def main(source, data, static_tables):
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
    }
    logger.info("loading_to_postgres")
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_queries["reports"], data["report"])
        gen_ids["report"] = cursor.fetchone()[0]
        for page in data["pages"]:
            page["report_id"] = gen_ids["report"]
        for table in data["tables"]:
            table["report_id"] = gen_ids["report"]
        for datasource in data["datasources"]:
            datasource["report_id"] = gen_ids["report"]

            insert_query = gen_query("pages", data, returning=("ordinal", "id"))
        for page in data["pages"]:
            cursor.execute(insert_query, page)
            ret = cursor.fetchone()
            gen_ids["pages"][ret[0]] = ret[1]
        for visual in data["visuals"]:
            visual["page_id"] = gen_ids["pages"][visual["page_ordinal"]]
            for c in ["page_ordinal", "filters", "selects"]:
                del visual[c]

        insert_query = gen_query("visuals", data)
        for visual in data["visuals"]:
            cursor.execute(insert_query, visual)
            ret = cursor.fetchone()
            gen_ids["visuals"][ret[0]] = ret[1]

        insert_query = gen_query("datasources", data)
        for datasource in data["datasources"]:
            cursor.execute(insert_query, datasource)
            ret = cursor.fetchone()
            gen_ids["datasources"][ret[0]] = ret[1]
        for table in data["tables"]:
            table["datasourceID"] = gen_ids["datasources"][table["datasourceID"]]

        insert_query = gen_query("tables", data)
        for table in data["tables"]:
            cursor.execute(insert_query, table)
            ret = cursor.fetchone()
            gen_ids["tables"][ret[0]] = ret[1]
        for column in data["columns"]:
            column["TableID"] = gen_ids["tables"][column["TableID"]]
        for measure in data["measures"]:
            measure["TableID"] = gen_ids["tables"][measure["TableID"]]

        insert_query = gen_query("columns", data)
        for column in data["columns"]:
            column["data_type"] = static_tables["datatypes"][column["data_type"]]
            cursor.execute(insert_query, column)
            ret = cursor.fetchone()
            gen_ids["columns"][ret[0]] = ret[1]

        insert_query = gen_query("measures", data)
        for measure in data["measures"]:
            cursor.execute(insert_query, measure)
            ret = cursor.fetchone()
            gen_ids["measures"][ret[0]] = ret[1]

        for dependency in data["dax_dependencies"]:
            get_ids(dependency)
            cursor.execute(insert_queries["dax_dependencies"], dependency)
        conn.commit()


if __name__ == "__main__":
    main()
