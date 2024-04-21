from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")


# API Examples =================================================================
@app.route("/")
def homepage():
    # If the return statement is a string, Flask will return it as an HTML
    # page when you hit the endpoint.
    return "<p>This is the root.</p>"


@app.route("/example")
def serve_example_json():
    # Use the `jsonify` function to return anything in the form of a JSON
    # object. Flask can handle encoding a very surprising number of things; if
    # it can't be encoded, Flask will raise an error.
    return jsonify({"firstElem": 1, "secondElem": "Foo"})


# To add an argument to the route, use <{type:}argname>. The `type:` at the
# start is optional, but good practice. Then, pass an argument with the same
# `argname` into the function, and Flask will automatically handle the binding.
@app.route("/example/<int:argument>", methods=["GET"])
def serve_example_with_argument(argument):
    return jsonify({"firstElem": argument, "secondElem": "Foo"})


# The Flask `request` object contains the request itself, including both
# metadata like the method ("GET", "POST", etc.) and the contents of the
# request. You can use it to bind to API calls like so.
@app.route("/example/hello", methods=["POST"])
def create_example_and_log_it():
    try:
        data = request.get_json()
    except:
        return "Bad req", 400

    name = data.get("name", None)
    return jsonify({"message": f"Hello, {name}."})
