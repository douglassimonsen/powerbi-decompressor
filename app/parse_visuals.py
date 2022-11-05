import zipfile
import json
from pprint import pprint

with zipfile.ZipFile('api.pbix') as zf:
    data = json.loads(zf.open('Report/Layout', 'r').read().decode('utf-16-le'))


def find_source(data):
    if not isinstance(data, dict):
        return
    if 'SourceRef' in data.get('Expression', {}):
        return data
    for v in data.values():            
        ret = find_source(v)
        if ret is not None:
            return ret


for section in data['sections']:
    section_info = {
        'section_name': section['name'],
        'ordinal': section['ordinal'],
    }
    for visual in section['visualContainers']:
        ret = {
            'height': visual['height'],
            'width': visual['width'],
            'x': visual['x'],
            'y': visual['y'],
            'z': visual['z'],
        }
        # filters
        # query
        # config
        ret['filters'] = []
        ret['selects'] = []
        for f in json.loads(visual['dataTransforms'])['queryMetadata']['Filters']:
            ret['filters'].append(find_source(f))
        for f in json.loads(visual['dataTransforms'])['selects']:
            ret['selects'].append(find_source(f))
