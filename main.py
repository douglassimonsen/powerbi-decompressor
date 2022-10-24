from sys import path; path.append('\\Program Files\\Microsoft.NET\\ADOMD.NET\\150')
import os
from pyadomd import Pyadomd

xmls = {
    f[:-4]: open(f'xmla/{f}').read()
    for f in os.listdir('xmla')
}

conn_str = 'Provider=MSOLAP;Data Source=localhost:61324;Catalog=15dfc18a-0908-493c-8f21-8162ba250dab;'


def load_pbix():
    with Pyadomd(conn_str) as conn:  # need to generate a random GUID
        conn.cursor().executeNonQuery(xmls['image_load'])


def save_pbix():
    with Pyadomd(conn_str) as conn:
        conn.cursor().executeNonQuery(xmls['image_save'])


def main():
    save_pbix()
    load_pbix()


if __name__ == '__main__':
    main()