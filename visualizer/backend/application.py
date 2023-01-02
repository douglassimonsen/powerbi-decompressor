from app import app
from static import routes
from pprint import pprint
from urllib.parse import parse_qs


def lambda_handler(event, context):
    method_name = event["requestContext"]["http"]["method"].lower()
    if method_name == "options":
        return {
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type, access-control-allow-origin",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST",
            }
        }
    method = getattr(lambda_client, method_name)
    x = method(
        event["rawPath"], json={k: v[0] for k, v in parse_qs(event["body"]).items()}
    )
    headers = dict(x.headers)
    headers["Content-Type"] = headers.get("Content-Type", "application/json")
    return {
        "statusCode": 200,
        "body": x.text,
        "headers": headers,
    }


lambda_client = app.test_client()
if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
