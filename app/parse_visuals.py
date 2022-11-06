import zipfile
import json
from pprint import pprint


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
    ret = {
        "pages": [],
        "visuals": [],
    }
    for section in data["sections"]:
        page_info = {
            "name": section["displayName"],
            "ordinal": section["ordinal"],
        }
        ret["pages"].append(page_info)
        for visual in section["visualContainers"]:
            visual["config"] = json.loads(visual["config"])
            visual_info = {
                "pbi_id": visual["config"]["name"],
                "height": visual["height"],
                "width": visual["width"],
                "x": visual["x"],
                "y": visual["y"],
                "z": visual["z"],
                "page_ordinal": page_info["ordinal"],
                "visual_type": visual["config"]["singleVisual"]["visualType"],
            }
            ret["visuals"].append(visual_info)
            visual_info["filters"] = []
            visual_info["selects"] = []
            if "dataTransforms" in visual:
                visual["dataTransforms"] = json.loads(visual["dataTransforms"])
                for f in visual["dataTransforms"]["queryMetadata"].get("Filters", []):
                    visual_info["filters"].append(find_source(f))
                for f in visual["dataTransforms"]["selects"]:
                    visual_info["selects"].append(find_source(f))
    return ret


if __name__ == "__main__":
    with zipfile.ZipFile("api.pbix") as zf:
        data = json.loads(zf.open("Report/Layout", "r").read().decode("utf-16-le"))

    pprint(main(data))
