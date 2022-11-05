import parse_datasources
import parse_visuals
import json
import zipfile


def extract_data(source):
    ret = {}
    with zipfile.ZipFile('api.pbix') as zf:
        ret['layout'] = json.loads(zf.open('Report/Layout', 'r').read().decode('utf-16-le'))

    with open('test.json') as f:
        ret['data_model'] = json.load(f)
    return ret


def get_visual_datasource_columns(data):
    datasource_dict = {
        x['name']: x['pbi_id']
        for x in data['datasources']
    }
    datasource_column_dict = {}
    for c in data['columns']:
        datasource_column_dict.setdefault(c['datasource_pbi_id'], {})[c['name']] = c['pbi_id']
    ret = []
    for visual in data['visuals']:
        for ds in visual['selects']:
            ds_name = ds['Expression']['SourceRef']['Entity']
            ds_column_name = ds['Property']
            ret.append({
                'visual_pbi_id': visual['pbi_id'],
                'datasource_column_pbi_id': datasource_column_dict[datasource_dict[ds_name]][ds_column_name],
                'visual_use': 'select',
            })
        for ds in visual['filters']:
            ds_name = ds['Expression']['SourceRef']['Entity']
            ds_column_name = ds['Property']
            ret.append({
                'visual_pbi_id': visual['pbi_id'],
                'datasource_column_pbi_id': datasource_column_dict[datasource_dict[ds_name]][ds_column_name],
                'visual_use': 'filter',
            })
    return ret


def main(source):
    raw_data = extract_data(source)
    data = parse_datasources.main(raw_data['data_model'])
    data = {**data, **parse_visuals.main(raw_data['layout'])}
    data['visual_datasource_columns'] = get_visual_datasource_columns(data)
    return data


if __name__ == '__main__':
    main('')