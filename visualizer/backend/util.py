import psycopg2
from pathlib import Path
import json
import os


creds = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
}
for i in range(2):
    candidate = Path(__file__).parents[i] / "creds.json"
    if os.path.exists(candidate):
        creds = json.load(open(candidate))["db"]
        break


def get_conn():
    return psycopg2.connect(**creds)


def read_query(query, kwargs):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(query, kwargs)
        columns = [x[0] for x in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


if __name__ == "__main__":
    get_conn()
