from pathlib import Path
import json
import boto3
import subprocess
import structlog
import os

logger = structlog.get_logger()
MIME_TYPES = {
    "js": "application/javascript",
    "css": "text/css",
    "html": "text/html",
    "ico": "image/x-icon",
}


def save_config():
    ssm = boto3.client("ssm")
    ret = {
        "db": json.loads(ssm.get_parameter(Name="db")["Parameter"]["Value"]),
        "website": json.loads(ssm.get_parameter(Name="website")["Parameter"]["Value"]),
    }
    with open(Path(__file__).parents[1] / "creds.json", "w") as f:
        json.dump(ret, f, indent=4)
    return ret


def deploy_vue(config):
    working_dir = Path(__file__).parents[1] / "visualizer" / "frontend"
    subprocess.run(["npm", "run", "build"], cwd=str(working_dir), shell=True)
    s3 = boto3.client("s3")
    prefix_len = len(str(working_dir / "dist")) + 1
    for folder, _, files in os.walk(working_dir / "dist"):
        for f in files:
            filename = os.path.join(folder, f)
            key = filename[prefix_len:].replace("\\", "/")
            mime_type = MIME_TYPES[filename.split(".")[-1]]
            logger.info(
                "loading websites",
                file=key,
                bucket=config["website"]["bucket"],
                mime_type=mime_type,
            )
            s3.upload_file(
                Filename=filename,
                Bucket=config["website"]["bucket"],
                Key=key,
                ExtraArgs={"ContentType": mime_type},
            )


def main():
    config = save_config()
    deploy_vue(config)


if __name__ == "__main__":
    main()
