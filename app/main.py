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
    source_dir = "C:/Users/mwham/Documents/repos/powerbi-decompressor/pbis"
    for f in os.listdir(source_dir):
        ret.append(os.path.join(source_dir, f))
    return ret


def main():
    initialize_db()
    pbis = get_pbis()
    for pbi_path in pbis:
        data = parse_pbi.main(pbi_path)
        load_data.main(pbi_path, data)


if __name__ == "__main__":
    main()
