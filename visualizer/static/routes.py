from app import app
import util
import flask
import os, pathlib

query_folder = pathlib.Path(__file__).parent / 'queries'
queries = {
    f[:-4]: open(query_folder / f).read()
    for f in os.listdir(query_folder)
    if f.endswith(".sql")
}


@app.route('/api/<query>', methods=['GET', 'POST'])
def reports(query):
    args = flask.request.get_json() or []
    return flask.jsonify(
        util.read_query(queries[query].format(*args))
    )