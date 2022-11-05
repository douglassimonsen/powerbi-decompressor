import util
import parse_pbi
import load_data
import os, pathlib; os.chdir(pathlib.Path(__file__).parent)
schema = open('schema.sql').read()


def initialize_db():
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        conn.commit()    


def main():
    initialize_db()
    source = 'dummy'
    data = parse_pbi.main(source)
    load_data.main(source, data)


if __name__ == '__main__':
    main()