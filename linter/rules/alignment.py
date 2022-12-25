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
