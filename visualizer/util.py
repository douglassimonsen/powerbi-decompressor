import psycopg2


def get_conn():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="postgres",
    )


def read_query(query):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
