import parse_datasources
import parse_visuals
import parse_dependencies
import json
import zipfile
import extract_library
import extract_library.dax_parser
from pprint import pprint
import structlog

logger = structlog.getLogger()


def extract_data(source):
    ret = {}
    with zipfile.ZipFile(source) as zf:
        ret["layout"] = json.loads(
            zf.open("Report/Layout", "r").read().decode("utf-16-le")
        )
    pbi = extract_library.PowerBi(source)
    ret["data_model"] = pbi.read_schema()
    return ret


def main(source, dump=False):
    raw_data = extract_data(source)
    if dump:
        with open("test.json", "w") as f:
            json.dump(raw_data, f, indent=4)

    data = parse_datasources.main(raw_data["data_model"])
    report_filters, visual_info = parse_visuals.main(raw_data["layout"])
    data = {
        **data,
        **visual_info,
        "reports": [
            {
                "file_path": source,
                "modified_time": raw_data["data_model"]["Model"][0]["ModifiedTime"],
                "pbi_id": str(raw_data["layout"]["reportId"])
                if "reportId" in raw_data["layout"]
                else None,
                "theme": raw_data["layout"].get("theme"),
                "layout_optimization": raw_data["layout"]["layoutOptimization"],
                "filters": report_filters,
                "culture": (raw_data["data_model"]["Culture"] or [{}])[0].get("Name"),
                "layout": json.dumps(
                    {
                        **raw_data["layout"],
                        "filters": None,
                        "sections": None,
                        "pods": None,
                        "config": None,
                    }
                ),
                "raw": json.dumps(raw_data["data_model"]["Model"]),
            }
        ],
    }
    data["dax_dependencies"] = parse_dependencies.main(data)
    return data


if __name__ == "__main__":
    main("")
