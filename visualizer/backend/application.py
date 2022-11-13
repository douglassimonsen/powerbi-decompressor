import flask
from app import app
from static import routes


if __name__ == "__main__":
    app.run(debug=True)
