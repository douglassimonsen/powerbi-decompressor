import os, pathlib
import util


insert_queries = {}
for f in os.listdir(pathlib.Path(__file__).parent / "queries"):
    insert_queries[f[:-4]] = open(pathlib.Path(__file__).parent / "queries" / f).read()


def main(source, data):
    gen_ids = {
        "report": None,
        "pages": {},
        "visuals": {},
        "datasources": {},
        "datasource_columns": {},
    }

    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_queries["reports"], {"name": source})
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

            page["report_id"] = gen_ids["report"]
            cursor.execute(insert_queries["datasources"], datasource)
            ret = cursor.fetchone()
            gen_ids["datasources"][ret[0]] = ret[1]

        for column in data["columns"]:
            column["datasource_id"] = gen_ids["datasources"][
                column["datasource_pbi_id"]
            ]
            cursor.execute(insert_queries["datasource_columns"], column)
            ret = cursor.fetchone()
            gen_ids["datasource_columns"][ret[0]] = ret[1]

        for visual_dsc in data["visual_datasource_columns"]:
            visual_dsc["visual_id"] = gen_ids["visuals"][visual_dsc["visual_pbi_id"]]
            visual_dsc["datasource_column_id"] = gen_ids["datasource_columns"][
                visual_dsc["datasource_column_pbi_id"]
            ]
            cursor.execute(insert_queries["visual_datasource_columns"], visual_dsc)

        conn.commit()


if __name__ == "__main__":
    main()
