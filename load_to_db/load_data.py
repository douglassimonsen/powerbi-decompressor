import os, pathlib
import util
import structlog
logger = structlog.getLogger()
insert_queries = {}
for f in os.listdir(pathlib.Path(__file__).parent / "queries"):
    insert_queries[f[:-4]] = open(pathlib.Path(__file__).parent / "queries" / f).read()


def main(source, data):
    gen_ids = {
        "report": None,
        "pages": {},
        'tables': {},
        'table_columns': {},
        "visuals": {},
        "datasources": {},
        "datasource_columns": {},
    }
    logger.info("loading_to_postgres")
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_queries["reports"], {"file_path": source})
        gen_ids["report"] = cursor.fetchone()[0]

        for page in data["pages"]:
            page["report_id"] = gen_ids["report"]
            cursor.execute(insert_queries["pages"], page)
            ret = cursor.fetchone()
            gen_ids["pages"][ret[0]] = ret[1]

        for visual in data["visuals"]:
            visual["page_id"] = gen_ids["pages"][visual["page_ordinal"]]
            cursor.execute(insert_queries["visuals"], visual)
            ret = cursor.fetchone()
            gen_ids["visuals"][ret[0]] = ret[1]

        for datasource in data["datasources"]:
            datasource["report_id"] = gen_ids["report"]
            datasource["source_type"] = None
            datasource["source_details"] = None
            cursor.execute(insert_queries["datasources"], datasource)
            ret = cursor.fetchone()
            gen_ids["datasources"][ret[0]] = ret[1]

        for table in data["tables"]:
            table["report_id"] = gen_ids["report"]
            table["datasourceID"] = gen_ids["datasources"][table["datasourceID"]]
            cursor.execute(insert_queries["tables"], table)
            ret = cursor.fetchone()
            gen_ids["tables"][ret[0]] = ret[1]

        for column in data["columns"]:
            column["table_id"] = gen_ids["tables"][
                column["TableID"]
            ]
            cursor.execute(insert_queries["table_columns"], column)
            ret = cursor.fetchone()
            gen_ids["table_columns"][ret[0]] = ret[1]

        for dependency in data["dax_dependencies"]:
            cursor.execute(insert_queries["dax_dependencies"], dependency)
        conn.commit()


if __name__ == "__main__":
    main()
