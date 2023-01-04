from app import app
from static import routes
from pprint import pprint
from urllib.parse import parse_qs
import json


def lambda_handler(event, context):
    def get_body_data(body):
        try:
            return json.loads(body)
        except:
            return {k: v[0] for k, v in parse_qs(event["body"]).items()}

    method_name = event["requestContext"]["http"]["method"].lower()
    if method_name == "options":
        return {
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Origin",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST",
            }
        }
    method = getattr(lambda_client, method_name)
    data = {
        **get_body_data(event["body"]),
        **event.get("queryStringParameters", {}),
    }
    x = method(event["rawPath"], json=data)
    headers = dict(x.headers)
    headers["Content-Type"] = headers.get("Content-Type", "application/json")
    return {
        "statusCode": 200,
        "body": x.text,
        "headers": headers,
    }


lambda_client = app.test_client()

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=3000)
