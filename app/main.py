import psycopg2
import parse_pbi
import os, pathlib; os.chdir(pathlib.Path(__file__).parent)
schema = open('schema.sql').read()


def get_conn():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname='postgres',
        user='postgres',
        password='postgres'
    )


def initialize_db():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        conn.commit()    


def main():
    initialize_db()
    source = ''
    data = parse_pbi.main(source)
    load_data.main(source, data)


if __name__ == '__main__':
    main()