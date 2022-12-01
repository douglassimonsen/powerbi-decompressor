import flask
import flask_cors

app = flask.Flask(__name__)
flask_cors.CORS(app, resource={"/*": {"origins": "*"}})


@app.after_request
def add_header_after(response):
    if flask.request.method.lower() != "options":
        response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.before_request
def add_header_before():
    if flask.request.method.lower() == "options":
        return flask.Response()
