import util
import parse_pbi
import load_data
import os, pathlib

os.chdir(pathlib.Path(__file__).parent)
schema = open("schema.sql").read()


def initialize_db():
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        conn.commit()


def get_pbis():
    ret = []
    source_dir = pathlib.Path(__file__).parents[1] / "pbis"
    for f in os.listdir(source_dir):
        if not f.endswith(".pbix"):
            continue
        ret.append(os.path.join(source_dir, f).replace("\\", "/"))
    return ret


def main():
    initialize_db()
    pbis = get_pbis()
    failed = 0
    for pbi_path in pbis:
        print(pbi_path)
        data = parse_pbi.main(pbi_path)
        load_data.main(pbi_path, data)
        try:
            data = parse_pbi.main(pbi_path)
            load_data.main(pbi_path, data)
        except:
            print("failed to load")
            failed += 1
    print(f"{failed} / {len(pbis)} failed")


if __name__ == "__main__":
    main()
