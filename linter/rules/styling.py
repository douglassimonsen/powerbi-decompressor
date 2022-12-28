from pprint import pprint

NOT_NULL = lambda x: x is not None


def get_font(val):
    ret = []
    if isinstance(val, list):
        candidates = [y for x in val for y in get_font(x)]
        ret.extend(filter(NOT_NULL, candidates))
    elif isinstance(val, dict):
        VALID_TEXT_OBJS = ["textRuns", "title"]
        candidates = []
        for k, v in val.items():
            if k in VALID_TEXT_OBJS:
                candidates.append({k: v})
            else:
                candidates.extend(get_font(v))
        ret.extend(filter(NOT_NULL, candidates))
    return ret


def consistent_fonts(page):
    for viz in page.visuals[:3]:
        font_info = get_font(viz.raw)
        pprint(font_info)
    exit()
