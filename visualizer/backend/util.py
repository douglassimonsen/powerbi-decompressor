import psycopg2
import boto3
import json
import structlog

logger = structlog.get_logger()


def get_creds():
    ssm = boto3.client("ssm")
    return json.loads(ssm.get_parameter(Name="db")["Parameter"]["Value"])


try:
    creds = get_creds()
except:
    logger.warn("Failed to get credentials")
    creds = {
        "host": "localhost",
        "port": 5432,
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
    }


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
