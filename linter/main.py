import psycopg2
import json
from pathlib import Path
from visual import Visual
from pprint import pprint


with open(Path(__file__).parents[1] / "creds.json") as f:
    creds = json.load(f)


def get_conn():
    return psycopg2.connect(**creds["db"])


def get_visuals():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("select * from pbi.visuals where page_id = 1")
        columns = [x[0] for x in cursor.description]
        data = [Visual(dict(zip(columns, row))) for row in cursor.fetchall()]

    border_checker(data)


def border_checker(data, threshold=5):
    SIDES = ["top", "right", "bottom", "left"]
    edge_dict = {k: {} for k in SIDES}
    for viz in data:
        edge_dict["top"].setdefault(viz.top, []).append(viz)
        edge_dict["right"].setdefault(viz.right, []).append(viz)
        edge_dict["bottom"].setdefault(viz.bottom, []).append(viz)
        edge_dict["left"].setdefault(viz.left, []).append(viz)

    nearly_matched = []
    for side in SIDES:
        previously_matched = False
        vals = list(sorted(edge_dict[side].keys()))
        for val1, val2 in zip(vals[:-1], vals[1:]):
            if val1 + threshold > val2:
                if previously_matched:
                    nearly_matched[-1]["vals"].append(val2)
                else:
                    nearly_matched.append({"side": side, "vals": [val1, val2]})
                previously_matched = True
            else:
                previously_matched = False
    pprint(nearly_matched)


def main():
    get_visuals()


if __name__ == "__main__":
    main()
