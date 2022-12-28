import psycopg2
from pathlib import Path
import json
import structlog

logger = structlog.get_logger()
LOCAL_CREDS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
}


def get_conn(db_creds=None):
    db_creds = db_creds or creds
    return psycopg2.connect(**db_creds)


def try_get_creds():
    try:
        creds = json.load(open(Path(__file__).parents[1] / "creds.json"))["db"]
        get_conn(creds)
    except FileNotFoundError:
        logger.warn("Can't find creds file, using default local db")
        return LOCAL_CREDS
    except psycopg2.OperationalError:
        logger.warn("DB connection issue, using default local db")
        return LOCAL_CREDS
    return creds


creds = try_get_creds()


if __name__ == "__main__":
    get_conn()
