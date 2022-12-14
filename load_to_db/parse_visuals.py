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
            # these two capture important information about hierarchy "columns"
            if "Level" in data.keys():
                ret["Level"] = data["Level"]
            if "Hierarchy" in data.keys() and isinstance(data["Hierarchy"], str):
                ret["Hierarchy"] = data["Hierarchy"]
            return ret


def main(data):
    def get_visual_type(vis_config):
        if "singleVisual" in vis_config:
            return vis_config["singleVisual"]["visualType"]
        elif "singleVisualGroup" in vis_config:
            return vis_config["singleVisualGroup"]["displayName"]
        else:
            logger.warning(
                "unparseable_visual", config=vis_config, visual=visual["config"]["name"]
            )

    report_filters = []
    ret = {"pages": [], "visuals": []}
    for f in json.loads(data.get("filters", "[]")):
        source = find_source(f)
        source = source if source is not None else f
        report_filters.append(source)
    for section in data["sections"]:
        page_info = {
            "name": section["displayName"],
            "ordinal": section.get(
                "ordinal", 0
            ),  # initial overview pages can be blank? 2018SU04 Blog Demo - April.pbix
            "width": section["width"],
            "height": section["height"],
            "display_option": section["displayOption"],
            "raw": json.dumps({**section, "visualContainers": None}),
            "filters": [],
            "config": section["config"],
        }
        page_info["pbi_id"] = page_info["ordinal"]

        for f in json.loads(section.get("filters", "[]")):
            source = find_source(f)
            source = source if source is not None else f
            page_info["filters"].append(source)
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
                "visual_type": get_visual_type(visual["config"]),
                "raw": json.dumps(visual),
                "drill_filter_other_visuals": visual.get("config", {})
                .get("singleVisual", {})
                .get("drillFilterOtherVisuals"),
            }
            ret["visuals"].append(visual_info)
            visual_info["filters"] = []
            visual_info["selects"] = []
            if "dataTransforms" in visual:
                visual["dataTransforms"] = json.loads(visual["dataTransforms"])
                visual["dataTransforms"]["queryMetadata"] = (
                    visual["dataTransforms"]["queryMetadata"] or {}
                )  # occasionally is null???
                for f in visual["dataTransforms"]["queryMetadata"].get("Filters", []):
                    source = find_source(f)
                    source = source if source is not None else f
                    visual_info["filters"].append(source)
                for f in visual["dataTransforms"]["selects"]:
                    source = find_source(f)
                    source = source if source is not None else f
                    visual_info["selects"].append(source)
    return report_filters, ret


if __name__ == "__main__":
    with zipfile.ZipFile("api.pbix") as zf:
        data = json.loads(zf.open("Report/Layout", "r").read().decode("utf-16-le"))

    pprint(main(data))
