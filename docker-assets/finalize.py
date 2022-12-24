import docker
from pathlib import Path
import json
import boto3
import base64
import structlog

logger = structlog.get_logger()


def build_docker_image():
    client = docker.from_env()
    logger.info("beginning to build", path=str(Path(__file__).parents[1]), tag="demo")
    client.images.build(
        path=str(Path(__file__).parents[1]),
        tag="demo",
        squash=False,
        quiet=False,
        platform="linux/arm64",
    )
    logger.info("finished build")


def save_config():
    ssm = boto3.client("ssm")
    db = ssm.get_parameter(Name="db")
    ecr = ssm.get_parameter(Name="ecr")
    ret = {
        "db": json.loads(db["Parameter"]["Value"]),
        "ecr": json.loads(ecr["Parameter"]["Value"]),
    }
    with open(Path(__file__).parents[1] / "creds.json", "w") as f:
        json.dump(ret, f, indent=4)
    return ret


def load_docker_image(config):
    image_url = f"{config['ecr']['url']}:latest"

    ecr = boto3.client("ecr", region_name="us-east-1")
    logger.info("getting ecr auth token")
    token = ecr.get_authorization_token(registryIds=[config["ecr"]["registry_id"]])
    username, password = (
        base64.b64decode(token["authorizationData"][0]["authorizationToken"])
        .decode()
        .split(":")
    )
    registry = token["authorizationData"][0]["proxyEndpoint"]

    client = docker.from_env()
    logger.info("logging into ecr")
    client.login(username, password, registry=registry)
    image = client.images.get("demo:latest")
    image.tag(image_url)
    logger.info("pushing to ecr", url=image_url)
    print(client.images.push(image_url))


def main():
    config = save_config()
    build_docker_image()
    load_docker_image(config)


if __name__ == "__main__":
    main()
