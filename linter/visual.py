class Visual:
    def __init__(self, raw) -> None:
        self.raw = raw
        self.top = raw["y"]
        self.bottom = raw["y"] + raw["height"]
        self.left = raw["x"]
        self.right = raw["x"] + raw["width"]


class Page:
    def __init__(self, raw) -> None:
        self.visuals = [Visual(viz_data) for viz_data in raw]


class Report:
    def __init__(self, raw) -> None:
        page_dict = {}
        for row in raw:
            page_dict.setdefault(row["page_id"], []).append(row)
        self.pages = [Page(page_data) for page_data in page_dict.values()]
