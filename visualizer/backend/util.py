import psycopg2
from pathlib import Path
import json


def get_conn():
    try:
        creds = json.load(open(Path(__file__).parents[2] / "creds.json"))["db"]
    except:
        creds = {
            "host": "localhost",
            "port": 5432,
            "dbname": "postgres",
            "user": "postgres",
            "password": "postgres",
        }
    return psycopg2.connect(**creds)


def read_query(query, kwargs):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(query, kwargs)
        columns = [x[0] for x in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


if __name__ == "__main__":
    get_conn()
