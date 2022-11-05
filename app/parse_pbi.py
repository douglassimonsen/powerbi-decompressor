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


def main(source):
    raw_data = extract_data(source)
    data = parse_datasources.main(raw_data['data_model'])
    data = {**data, **parse_visuals.main(raw_data['layout'])}
    return data


if __name__ == '__main__':
    main('')