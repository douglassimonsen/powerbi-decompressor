import parse_pbi
import load_data
import initialize_db
import os, pathlib
import structlog
import logging

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.WARN),
)
logger = structlog.getLogger()
os.chdir(pathlib.Path(__file__).parent)
schema = open("schema.sql").read()


def get_pbis():
    ret = []
    source_dir = pathlib.Path(__file__).parents[1] / "pbis"
    for f in os.listdir(source_dir):
        if not f.endswith(".pbix"):
            continue
        ret.append(os.path.join(source_dir, f).replace("\\", "/"))
    return ret


def main():
    static_tables = initialize_db.main()
    pbis = get_pbis()
    failed = 0
    for pbi_path in pbis[:3]:
        print(pbi_path)
        data = parse_pbi.main(pbi_path)
        load_data.main(data, static_tables)
    structlog.contextvars.clear_contextvars()
    logger.info("results", successes=len(pbis) - failed, failed=failed)


if __name__ == "__main__":
    main()

    # from auto_profiler import Profiler
    # with Profiler(depth=5):
    #     main()
