import docker
from pathlib import Path
import json
import boto3
import base64
import structlog

logger = structlog.get_logger()


def save_config():
    ssm = boto3.client("ssm")
    db = ssm.get_parameter(Name="db")
    ret = {"db": json.loads(db["Parameter"]["Value"])}
    with open(Path(__file__).parents[1] / "creds.json", "w") as f:
        json.dump(ret, f, indent=4)
    return ret


def main():
    config = save_config()


if __name__ == "__main__":
    main()
