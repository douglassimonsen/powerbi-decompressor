from app import app
import util
import flask
import os, pathlib

query_folder = pathlib.Path(__file__).parent / "queries"
queries = {
    f[:-4]: open(query_folder / f).read()
    for f in os.listdir(query_folder)
    if f.endswith(".sql")
}


@app.route("/api/query/<query>", methods=["GET", "POST"])
def reports(query):
    kwargs = (
        flask.request.get_json() or dict(flask.request.args) or {}
    )  # dict not really necessary, but prints nicer
    return flask.jsonify(util.read_query(queries[query], kwargs))


@app.route("/monitor/alive", methods=["GET", "POST"])
def alive():
    return "alive"


@app.route("/admin/creds", methods=["GET", "POST"])
def creds():
    return flask.jsonify(util.creds)
