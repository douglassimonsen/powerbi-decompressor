import docker
from pathlib import Path
import json
import boto3
import base64


def build_docker_image():
    client = docker.from_env()
    client.images.build(
        path=str(Path(__file__).parents[1]),
        tag="demo",
        squash=False,
        quiet=False,
        platform="linux/arm64",
    )


def get_config():
    ssm = boto3.client("ssm")
    db = ssm.get_parameter(Name="db")
    ecr = ssm.get_parameter(Name="ecr")
    return {
        "db": json.loads(db["Parameter"]["Value"]),
        "ecr": json.loads(ecr["Parameter"]["Value"]),
    }


def load_docker_image():
    data = get_config()
    image_url = f"{data['ecr']['url']}:latest"

    ecr = boto3.client("ecr", region_name="us-east-1")
    token = ecr.get_authorization_token(registryIds=[data["ecr"]["registry_id"]])
    username, password = (
        base64.b64decode(token["authorizationData"][0]["authorizationToken"])
        .decode()
        .split(":")
    )
    registry = token["authorizationData"][0]["proxyEndpoint"]

    client = docker.from_env()
    client.login(username, password, registry=registry)
    image = client.images.get("demo:latest")
    image.tag(image_url)
    print(client.images.push(image_url))


def main():
    build_docker_image()
    load_docker_image()


if __name__ == "__main__":
    main()
