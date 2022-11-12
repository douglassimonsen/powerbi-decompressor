import zipfile
import json
from pprint import pprint
import structlog
logger = structlog.getLogger()


def find_source(data):
    if not isinstance(data, dict):
        return
    if "SourceRef" in data.get("Expression", {}):
        return data
    for v in data.values():
        ret = find_source(v)
        if ret is not None:
            return ret


def main(data):
    def get_visual_type(vis_config):
        if 'singleVisual' in vis_config:
            return vis_config["singleVisual"]["visualType"]
        elif 'singleVisualGroup' in vis_config:
            return vis_config['singleVisualGroup']['displayName']
        else:
            logger.warning("unparseable_visual", config=vis_config)

    ret = {
        "pages": [],
        "visuals": [],
    }
    for section in data["sections"]:
        page_info = {
            "name": section["displayName"],
            "ordinal": section.get(
                "ordinal", 0
            ),  # initial overview pages can be blank? 2018SU04 Blog Demo - April.pbix
            "width": section["width"],
            "height": section["height"],
        }
        ret["pages"].append(page_info)
        for visual in section["visualContainers"]:
            visual["config"] = json.loads(visual["config"])
            visual_info = {
                "pbi_id": visual["config"]['name'],
                "height": visual["height"],
                "width": visual["width"],
                "x": visual["x"],
                "y": visual["y"],
                "z": visual["z"],
                "page_ordinal": page_info["ordinal"],
                "visual_type": get_visual_type(visual["config"]),
            }
            ret["visuals"].append(visual_info)
            visual_info["filters"] = []
            visual_info["selects"] = []
            if "dataTransforms" in visual:
                visual["dataTransforms"] = json.loads(visual["dataTransforms"])
                visual['dataTransforms']['queryMetadata'] = visual['dataTransforms']['queryMetadata'] or {}  # occasionally is null???
                for f in visual["dataTransforms"]["queryMetadata"].get("Filters", []):
                    visual_info["filters"].append(find_source(f))
                for f in visual["dataTransforms"]["selects"]:
                    visual_info["selects"].append(find_source(f))
    return ret


if __name__ == "__main__":
    with zipfile.ZipFile("api.pbix") as zf:
        data = json.loads(zf.open("Report/Layout", "r").read().decode("utf-16-le"))

    pprint(main(data))
