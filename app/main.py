import psycopg2
import parse_datasources
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


def main():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        conn.commit()
    data = 


if __name__ == '__main__':
    main()