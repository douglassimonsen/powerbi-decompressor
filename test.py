from sys import path; path.append('\\Program Files\\Microsoft.NET\\ADOMD.NET\\150')

from pyadomd import Pyadomd

conn_str = 'Provider=MSOLAP;Data Source=localhost:61324;Catalog=15dfc18a-0908-493c-8f21-8162ba250dab;'
query = """EVALUATE Kris"""

with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(query) as cur:
        print(cur.fetchall())