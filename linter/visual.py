class Visual:
    def __init__(self, raw) -> None:
        self.raw = raw
        self.id = raw["id"]
        self.top = raw["y"]
        self.bottom = raw["y"] + raw["height"]
        self.left = raw["x"]
        self.right = raw["x"] + raw["width"]


class Page:
    def __init__(self, raw) -> None:
        self.visuals = [Visual(viz_data) for viz_data in raw]
        self.width = raw[0]["page_width"]
        self.height = raw[0]["page_height"]


class Report:
    def __init__(self, raw) -> None:
        page_dict = {}
        for row in raw:
            page_dict.setdefault(row["page_id"], []).append(row)
        self.pages = [Page(page_data) for page_data in page_dict.values()]
