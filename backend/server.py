from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def homepage():
    return "<p>This is the root.</p>"


@app.route("/example")
def serve_example_json():
    return jsonify({"firstElem": 1, "secondElem": "Foo"})


@app.route("/example/<int:argument>", methods=["GET", "POST"])
def serve_example_with_argument(argument):
    return jsonify({"firstElem": argument, "secondElem": "Foo"})
