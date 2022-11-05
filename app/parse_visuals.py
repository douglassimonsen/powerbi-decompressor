import zipfile
import json
from pprint import pprint


def find_source(data):
    if not isinstance(data, dict):
        return
    if 'SourceRef' in data.get('Expression', {}):
        return data
    for v in data.values():            
        ret = find_source(v)
        if ret is not None:
            return ret


def main(data):
    ret = {
        'sections': [],
        'visuals': [],
    }
    for section in data['sections']:
        section_info = {
            'section_name': section['name'],
            'ordinal': section['ordinal'],
        }
        ret['sections'].append(section_info)
        for visual in section['visualContainers']:
            visual_info = {
                'height': visual['height'],
                'width': visual['width'],
                'x': visual['x'],
                'y': visual['y'],
                'z': visual['z'],
                'section_ordinal': section_info['ordinal'],
            }
            ret['visuals'].append(visual_info)
            visual_info['filters'] = []
            visual_info['selects'] = []
            if 'dataTransforms' in visual:
                for f in json.loads(visual['dataTransforms'])['queryMetadata'].get('Filters', []):
                    visual_info['filters'].append(find_source(f))
                for f in json.loads(visual['dataTransforms'])['selects']:
                    visual_info['selects'].append(find_source(f))
    return ret


if __name__ == '__main__':
    with zipfile.ZipFile('api.pbix') as zf:
        data = json.loads(zf.open('Report/Layout', 'r').read().decode('utf-16-le'))

    pprint(main(data))