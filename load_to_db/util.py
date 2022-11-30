import psycopg2
from pathlib import Path
import json


def get_conn():
    try:
        creds = json.load(open(Path(__file__).parents[1] / "creds.json"))["db"]
    except:
        creds = {
            "host": "localhost",
            "port": 5432,
            "dbname": "postgres",
            "user": "postgres",
            "password": "postgres",
        }
    return psycopg2.connect(**creds)


if __name__ == "__main__":
    get_conn()
