import util
import parse_pbi
import load_data
import os, pathlib
import structlog
import logging
import json

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.WARN),
)
logger = structlog.getLogger()
os.chdir(pathlib.Path(__file__).parent)
schema = open("schema.sql").read()


def initialize_db():
    def load_static_data(directory, file, cursor):
        table_name = file[:-5]
        config = json.load(open(directory / file))
        data = config["data"]
        columns = ", ".join(data[0].keys())
        values = ", ".join(f"%({x})s" for x in data[0].keys())
        cursor.executemany(
            f"insert into pbi.{table_name} ({columns}) values ({values})", data
        )

        cols = ", ".join(config["returning"])
        cursor.execute(f"select {cols} from pbi.{table_name}")
        return table_name, dict(cursor.fetchall())

    static_tables = {}
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        for f in os.listdir(pathlib.Path(__file__).parent / "static_data"):
            table_name, mapping = load_static_data(
                pathlib.Path(__file__).parent / "static_data", f, cursor
            )
            static_tables[table_name] = mapping
        conn.commit()
    return static_tables


def get_pbis():
    ret = []
    source_dir = pathlib.Path(__file__).parents[1] / "pbis"
    for f in os.listdir(source_dir):
        if not f.endswith(".pbix"):
            continue
        ret.append(os.path.join(source_dir, f).replace("\\", "/"))
    return ret


def main():
    static_tables = initialize_db()
    pbis = get_pbis()
    failed = 0
    for pbi_path in pbis:
        print(pbi_path)
        data = parse_pbi.main(pbi_path)
        load_data.main(pbi_path, data, static_tables)
    structlog.contextvars.clear_contextvars()
    logger.info("results", successes=len(pbis) - failed, failed=failed)


if __name__ == "__main__":
    main()
