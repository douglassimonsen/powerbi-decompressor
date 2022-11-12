import util
import parse_pbi
import load_data
import os, pathlib
import structlog
import logging
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.WARN),
)
logger = structlog.getLogger()
os.chdir(pathlib.Path(__file__).parent)
schema = open("schema.sql").read()


def initialize_db():
    logger.info("initializing_db")
    with util.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        conn.commit()


def get_pbis():
    logger.info("collecting_pbis")
    ret = []
    source_dir = pathlib.Path(__file__).parents[1] / "pbis"
    for f in os.listdir(source_dir):
        if not f.endswith(".pbix"):
            continue
        ret.append(os.path.join(source_dir, f).replace("\\", "/"))
    return ret


def main():
    initialize_db()
    pbis = get_pbis()
    failed = 0
    for pbi_path in pbis:
        logger.info("parsing_pbix")
        data = parse_pbi.main(pbi_path)
        load_data.main(pbi_path, data)
        try:
            data = parse_pbi.main(pbi_path)
            load_data.main(pbi_path, data)
        except Exception as e:
            logger.error("failed_to_load", error=e)
            failed += 1
    structlog.contextvars.clear_contextvars()
    logger.info("results", successes=len(pbis) - failed, failed=failed)


if __name__ == "__main__":
    main()
