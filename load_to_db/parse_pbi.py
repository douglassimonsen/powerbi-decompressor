import parse_datasources
import parse_visuals
import json
import zipfile
import extract_library
from pprint import pprint
import logging
logger = logging.getLogger()


def extract_data(source):
    ret = {}
    with zipfile.ZipFile(source) as zf:
        ret["layout"] = json.loads(
            zf.open("Report/Layout", "r").read().decode("utf-16-le")
        )
    pbi = extract_library.PowerBi(source)
    ret["data_model"] = pbi.read_schema()
    return ret


def discover_dependencies(data):
    def get_parents(expr, child_id, child_type):
        """
        TODO: fix with lark
        """
        ret = []
        for parent_name, info in parents.items():
            if parent_name in expr:
                ret.append({**info, "child": child_id, "child_type": child_type})
        return ret

    dependencies = []
    parents = {
        **{x['name']: {"child_id": x["pbi_id"], "child_type": "measure"}
        for x in data['measures']
        if x['name'] is not None
        },
        **{x['name']: {"child_id": x["pbi_id"], "child_type": "column"}
        for x in data['columns']
        if x['name'] is not None            
        },
    }
    for column in data['columns']:
        if column['Expression'] is None:
            continue
        dependencies.extend(
            get_parents(column['Expression'], column['pbi_id'], 'column')
        )
    
    for column in data['measures']:
        dependencies.extend(
            get_parents(column['Expression'], column['pbi_id'], 'measure')
        )
    
    table_dict = {x['pbi_id']: x['name'] for x in data['tables']}
    parents = {
        **{
            (table_dict[x['TableID']], x['name']): {
                "child_id": x['pbi_id'],
                "child_type": "measure"
            }
            for x in data["measures"]
        },
        **{
            (table_dict[x['TableID']], x['name']): {
                "child_id": x['pbi_id'],
                "child_type": "column"
            }
            for x in data["columns"]
        }
    }
    for visual in data['visuals']:
        for ds in visual['selects']:
            ds_name = ds['Expression']['SourceRef']['Entity']
            ds_column_name = ds['Property']
            if (ds_name, ds_column_name) not in parents:
                logger.warning(f"{(ds_name, ds_column_name)} not in parents")
                continue
            dependencies.append({
                "parent_id": visual['pbi_id'],
                "parent_type": "table",
                "depdency_type": "visual_select",
                **parents[(ds_name, ds_column_name)],
            })
        for ds in visual['filters']:
            ds_name = ds['Expression']['SourceRef']['Entity']
            ds_column_name = ds['Property']
            if (ds_name, ds_column_name) not in parents:
                logger.warning(f"{(ds_name, ds_column_name)} not in parents")
                continue
            dependencies.append({
                "parent_id": visual['pbi_id'],
                "parent_type": "table",
                "depdency_type": "visual_filter",
                **parents[(ds_name, ds_column_name)],
            })


def main(source):
    raw_data = extract_data(source)
    with open("test.json", "w") as f:
        json.dump(raw_data, f, indent=4)

    data = parse_datasources.main(raw_data["data_model"])
    data = {**data, **parse_visuals.main(raw_data["layout"])}
    data["dax_dependencies"] = discover_dependencies(data)
    return data


if __name__ == "__main__":
    main("")
