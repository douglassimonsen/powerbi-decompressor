import zipfile
import json
from pprint import pprint

with zipfile.ZipFile('api.pbix') as zf:
    data = json.loads(zf.open('Report/Layout', 'r').read().decode('utf-16-le'))

for section in data['sections']:
    section_info = {
        'section_name': section['name'],
        'ordinal': section['ordinal'],
    }
    for visual in section['visualContainers']:
        visual = {
            'height': visual['height'],
            'weight': visual['weight'],
            'x': visual['x'],
            'y': visual['y'],
            'z': visual['z'],
        }
        # dataTransforms
        # filters
        # query
        # config
        pprint(visual['dataTransforms'])
        exit()
