import json
from pprint import pprint


def get_datasources(tables):
    ret = []
    for table in tables:
        ret.append({
            'pbi_id': table['ID'],
            'name': table['Name']
        })
    return ret


def get_datasource_columns(columns):
    ret = []
    for column in columns:
        ret.append({
            'pbi_id': column['ID'],
            'datasource_pbi_id': column['TableID'],
            'data_type': column['ExplicitDataType'],
            'name': column.get('ExplicitName'),
            'isHidden': column.get('isHidden', False)
        })
    return ret


def main(data):
    datasources = get_datasources(data['Table'])
    columns = get_datasource_columns(data['Column'])
    return {
        'datasources': datasources,
        'columns': columns
    }


if __name__ == '__main__':
    with open('test.json') as f:
        data = json.load(f)
    main(data)
