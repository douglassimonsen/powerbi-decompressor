import util
import os, pathlib
import structlog
import json
import toposort

logger = structlog.getLogger()
dependencies = {
    "column_dependency_counts.sql": {"root_parents.sql"},
    "measure_dependency_counts.sql": {"root_parents.sql"},
    "drill_dependencies.sql": {"root_parents.sql"},
}


def get_files():
    ret = {"schema": None, "views": [], "static_tables": {}}

    working_dir = pathlib.Path(__file__).parent

    ret["schema"] = open(working_dir / "schema.sql").read()

    files = os.listdir(working_dir / "views")
    files = {f: dependencies.get(f, set()) for f in files}
    files = toposort.toposort_flatten(files)
    for f in files:
        ret["views"].append(open(working_dir / "views" / f).read())

    for f in os.listdir(working_dir / "static_data"):
        ret["static_tables"][f[:-5]] = json.load(open(working_dir / "static_data" / f))

    return ret


def load_static_data(table_name, config, cursor):
    data = config["data"]
    columns = ", ".join(data[0].keys())
    values = ", ".join(f"%({x})s" for x in data[0].keys())
    cursor.executemany(
        f"insert into pbi.{table_name} ({columns}) values ({values})", data
    )
    cols = ", ".join(config["returning"])
    cursor.execute(f"select {cols} from pbi.{table_name}")
    return dict(cursor.fetchall())


def main():
    data = get_files()
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(data["schema"])
        for v in data["views"]:
            cursor.execute(v)
        for name, table in data["static_tables"].items():
            data["static_tables"][name] = load_static_data(name, table, cursor)
        conn.commit()
    return data["static_tables"]


if __name__ == "__main__":
    main()
