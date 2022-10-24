import bs4
import json


def handle_child(doc):
    def clean(records):
        if isinstance(records, dict):
            return {k.strip(): clean(v) for k, v in records.items()}
        elif isinstance(records, list):
            return [clean(v) for v in records]
        elif isinstance(records, str):
            return records.strip()

    section = []
    for row in doc.find_all("row"):
        row_dict = {}
        for field in row:
            if field.name is None:
                continue
            val = field.text
            try:
                val = json.loads(val)
            except:
                pass

            row_dict[field.name] = val
        section.append(row_dict)

    section = clean(section)
    if len(section) == 0:
        return {}
    elif len(section) == 1:
        return section[0]
    else:
        return section


def parse_schema(schema):
    full_schema = {}
    if not isinstance(schema, bs4.BeautifulSoup):
        schema = bs4.BeautifulSoup(schema, "xml")
    for child in schema.results:
        if not isinstance(child, bs4.element.Tag):
            continue
        if "name" not in child.attrs:
            continue
        full_schema[child["name"]] = handle_child(child)
    return full_schema


if __name__ == "__main__":
    parse_schema(open("test.xml").read())
