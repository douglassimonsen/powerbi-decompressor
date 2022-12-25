from pprint import pprint


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
    results = []
    for ret in nearly_matched:
        results.append(
            {
                "side": ret["side"],
                "visuals": [
                    viz.id for val in ret["vals"] for viz in edge_dict[ret["side"]][val]
                ],
                "correct_val": round(sum(ret["vals"]) / len(ret["vals"]), 3),
            }
        )
    return results


def page_alignment(page):
    def nearby(edge, ave, side):
        THRESHOLD = 25
        if side in ("bottom", "right"):
            return 0 < edge - ave < THRESHOLD
        else:
            return -THRESHOLD < edge - ave < 0

    fractions = [1 / 4, 1 / 3, 1 / 2, 2 / 3, 3 / 4]
    height_vals = [frac * page.height for frac in fractions]
    width_vals = [frac * page.width for frac in fractions]
    symmetry_vals = {
        "top": height_vals,
        "bottom": height_vals,
        "left": width_vals,
        "right": width_vals,
    }
    symmetry_dir = {
        "top": "y",
        "bottom": "y",
        "left": "x",
        "right": "x",
    }

    edge_dict = {"x": {}, "y": {}}
    matching_edges = {}
    for viz in page.visuals:
        for edge in ["top", "bottom", "left", "right"]:
            val = getattr(viz, edge)
            for v in symmetry_vals[edge]:
                if nearby(val, v, edge):
                    matching_edges.setdefault((v, symmetry_dir[edge]), []).append(
                        [val, edge, viz]
                    )
    results = []
    for (ax_point, _), nearby_points in matching_edges.items():
        distances = [abs(ax_point - x[0]) for x in nearby_points]
        ave_dist = round(sum(distances) / len(distances), 2)
        for (val, edge, viz) in nearby_points:
            correct_val = round(
                (ax_point + ave_dist)
                if edge in ("bottom", "right")
                else (ax_point - ave_dist),
                2,
            )
            if getattr(viz, edge) == correct_val:
                continue
            results.append(
                {
                    "side": edge,
                    "visual": viz.id,
                    "correct_val": correct_val,
                    "old_val": getattr(viz, edge),
                    "ax_point": ax_point,
                    "ave_dist": ave_dist,
                }
            )
    return results
