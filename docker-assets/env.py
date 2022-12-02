import boto3
import time
import structlog
from pathlib import Path
import json
import docker

logger = structlog.get_logger()


cloudformation = boto3.client("cloudformation")
rds = boto3.client("rds")


def check_stack_status(stack_name: str) -> str:
    stacks = cloudformation.list_stacks(
        StackStatusFilter=[
            "CREATE_IN_PROGRESS",
            "CREATE_FAILED",
            "CREATE_COMPLETE",
            "ROLLBACK_IN_PROGRESS",
            "ROLLBACK_FAILED",
            "ROLLBACK_COMPLETE",
            "DELETE_IN_PROGRESS",
            "DELETE_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
            "UPDATE_COMPLETE",
            "UPDATE_FAILED",
            "UPDATE_ROLLBACK_IN_PROGRESS",
            "UPDATE_ROLLBACK_FAILED",
            "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
            "UPDATE_ROLLBACK_COMPLETE",
            "REVIEW_IN_PROGRESS",
            "IMPORT_IN_PROGRESS",
            "IMPORT_COMPLETE",
            "IMPORT_ROLLBACK_IN_PROGRESS",
            "IMPORT_ROLLBACK_FAILED",
            "IMPORT_ROLLBACK_COMPLETE",
        ]
    )["StackSummaries"]
    for stack in stacks:
        if stack["StackName"] == stack_name:
            return stack["StackStatus"]


def build_stack(stack: str) -> None:
    if check_stack_status(stack) is not None:
        logger.error("Stack already exists")
        raise ValueError("Stack already exists")

    start = time.time()
    cloudformation.create_stack(
        StackName=stack,
        TemplateBody=open(Path(__file__).parent / "cloudformation.yaml").read(),
        OnFailure="DELETE",
        Capabilities=["CAPABILITY_IAM"],
    )

    while check_stack_status(stack) == "CREATE_IN_PROGRESS":
        logger.debug("Waiting for stack")
        time.sleep(5)

    final_status = check_stack_status(stack)
    if final_status != "CREATE_COMPLETE":
        logger.error(f"The formation completed with status: {final_status}.")
        raise ValueError(f"The formation completed with status: {final_status}.")
    logger.info(
        f"Stack creation took {round(time.time() - start, 2)} seconds to complete"
    )


def get_stack_resources(stack: str) -> tuple[str, str, list[dict]]:
    resources = cloudformation.list_stack_resources(StackName=stack)[
        "StackResourceSummaries"
    ]
    ret = {}
    for resource in resources:
        if resource["ResourceType"] == "AWS::RDS::DBInstance":
            data = rds.describe_db_instances(
                DBInstanceIdentifier=resource["PhysicalResourceId"]
            )["DBInstances"][0]
            ret["db"] = {
                "host": data["Endpoint"]["Address"],
                "port": data["Endpoint"]["Port"],
                "dbname": data["DBName"],
                "user": data["MasterUsername"],
                "password": "postgres",
            }
        elif resource["ResourceType"] == "AWS::ECR::Repository":
            ret["ecr"] = {"id": resource["PhysicalResourceId"]}
    return ret


def load_docker_image(resources):
    client = docker.from_env()
    client.images.build(
        path=str(Path(__file__).parents[1]), tag="website", squash=True, quiet=False
    )


def create_stack(stack: str) -> None:
    # build_stack(stack)
    resources = get_stack_resources(stack)
    # with open(Path(__file__).parents[1] / "creds.json", "w") as f:
    #     json.dump(resources, f, indent=2)
    load_docker_image(resources)


def delete_stack(stack: str) -> None:
    cloudformation.delete_stack(StackName=stack)


if __name__ == "__main__":
    create_stack("powerbi-parser2")
    # delete_stack()
