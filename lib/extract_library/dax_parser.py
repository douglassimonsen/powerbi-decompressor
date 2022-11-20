import re
from typing import List, Dict

template = re.compile(r"(?P<table>(\w+)|('[^']+'))?(?P<column>\[[^\[\]]+\])(?P<hierarchy>\.\[[^\[\]]+\])?")


def get_variables(dax_statement: str) -> List[Dict[str, str]]:
    """
    The template contains named capture groups for legibility, but not currently being used
    first looks like either "Table1" or 'table 1', so we need to strip off any possible "'"s
    second looks like [Column Name]
    third looks like .[Hierarchy Name]
    Matches look like [(table), (table if single word), (table if parenthesis), (column), (hierarchy)]
    """

    matches = re.findall(template, dax_statement)

    return list({
        (m[0].strip("'"), m[3][1:-1], m[4][2:-1])
        for m in matches
    })


if __name__ == "__main__":
    import json
    from pathlib import Path

    with open(Path(__file__).parent / "test.json") as f:
        data = json.load(f)
    for row in set(data):
        print('\n' * 2)
        print(row)
        print(get_variables(row))
