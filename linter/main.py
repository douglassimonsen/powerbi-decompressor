import psycopg2
import json
from pathlib import Path
import visual
from pprint import pprint
import os
from rules import alignment
import structlog

logger = structlog.get_logger()

QUERIES = {
    f[:-4]: open(Path(__file__).parent / "queries" / f).read()
    for f in os.listdir(Path(__file__).parent / "queries")
    if f.endswith(".sql")
}


with open(Path(__file__).parents[1] / "creds.json") as f:
    creds = json.load(f)


def get_conn():
    return psycopg2.connect(**creds["db"])


def get_visuals():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(QUERIES["base"])
        columns = [x[0] for x in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return visual.Report(data)


def main():
    results = {"in-page alignment": []}
    report = get_visuals()
    for page in report.pages:
        results["in-page alignment"].extend(alignment.border_checker(page.visuals))
    results["all-report alignment"] = alignment.border_checker(
        [viz for page in report.pages for viz in page.visuals]
    )
    for rule, hits in results.items():
        for hit in hits:
            logger.info(rule, **hit)


if __name__ == "__main__":
    main()
