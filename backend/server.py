import sqlite3
from os.path import join as pathjoin
from pathlib import Path

from flask import Flask, g, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

# Database Example =============================================================

# Because I intend for this example to work on both Windows and Unix systems,
# we need to use a method to build paths, since Windows uses "\" and Unix uses
# "/", etc. If you were using this for an actual application, you'd probably
# be deploying to a specific Linux environment, so you wouldn't need to do
# this path stuff.
DATABASE = pathjoin(Path(__file__).parent, "sqlite3.db")


# `g` is the Flask global application namespace. Read this method as "If there
# is a database already assigned to Flask, use the existing database;
# otherwise, create a new database and assign it to Flask."
def get_or_create_db():
    db = getattr(g, "database", None)
    if db is None:
        # Open a new connection to DATABASE
        db = sqlite3.connect(DATABASE)

        # Specify that we want the DB to return rows in this form:
        #   { column1: value1, column2: value2, etc. }
        # so that it is easy to parse to JSON
        def jsonlike_rows(cursor, row):
            return {
                cursor.description[index][0]: value for index, value in enumerate(row)
            }

        db.row_factory = jsonlike_rows

        # Lastly, assign it to the name "database" inside of `g`, so that
        # next time we don't create a new connection again.
        g.database = db

    return db


# This is a wrapper function to make querying the DB easier. Using this allows
# you to write `query("SELECT * FROM table")` and just use that, instead of
# having to deal with cursors and whatnot every time you want to get data.
def query(querystring: str, args=[], limit: int | None = None) -> list:
    db = get_or_create_db()
    cursor = db.cursor()
    cursor.execute(querystring, args)
    results = cursor.fetchall()
    cursor.close()

    if limit is not None and limit > 0:
        results = results[0:limit]

    return results


# The `app.teardown_appcontext` decorator means that this function will execute
# when the server is ordered to shut down. This just cleans up the connection
# to make sure that there's nothing left hanging after the app stops running.
@app.teardown_appcontext
def close_connections(_):
    db = getattr(g, "database", None)
    if db is not None:
        db.close()
        g.database = None


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


# To show how the database works, this is a method that just returns the list
# of fruits.
@app.route("/fruits")
def get_all_fruits():
    return jsonify(query("SELECT * FROM fruits"))


@app.route("/fruits/<int:fruit_id>")
def get_specific_fruit(fruit_id):
    result = query("SELECT * FROM fruits WHERE fruit_id=?", [fruit_id], limit=1)
    try:
        fruit = result[0]
    except IndexError:
        # There is no element 0, so there was no match
        return (jsonify({"message": f"No fruit with id {fruit_id} found"}), 204)
    return jsonify({"message": "Success", "fruit": fruit})
