import os, pathlib
import util


insert_queries = {}
for f in os.listdir(pathlib.Path(__file__).parent / 'queries'):
    insert_queries[f[:-4]] = open(pathlib.Path(__file__).parent / 'queries' / f).read()


def main(source, data):
    gen_ids = {
        'report': None,
        'pages': {}
    }

    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_queries['reports'], {'name': source})
        gen_ids['report'] = cursor.fetchone()[0]

        for page in data['pages']:
            page['report_id'] = gen_ids['report']
            cursor.execute(insert_queries['pages'], page)
            ret = cursor.fetchone()
            gen_ids['pages'][ret[0]] = ret[1]

if __name__ == '__main__':
    main()