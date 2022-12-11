import psycopg2
from pathlib import Path
import json


try:
    creds = json.load(open(Path(__file__).parents[1] / "creds.json"))["db"]
    raise BaseException
except:
    creds = {
        "host": "localhost",
        "port": 5432,
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
    }


def get_conn():
    return psycopg2.connect(**creds)


if __name__ == "__main__":
    get_conn()
