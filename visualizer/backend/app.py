import flask
import flask_cors

app = flask.Flask(__name__)
flask_cors.CORS(app, resource={
    "/*":{
        "origins":"*"
    }
})