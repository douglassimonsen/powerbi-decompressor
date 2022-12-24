class Visual:
    def __init__(self, raw) -> None:
        self.raw = raw
        self.top = raw["y"]
        self.bottom = raw["y"] + raw["height"]
        self.left = raw["x"]
        self.right = raw["x"] + raw["width"]


class Page:
    def __init__(self, raw) -> None:
        pass


class Report:
    def __init__(self, raw) -> None:
        pass
