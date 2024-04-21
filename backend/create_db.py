import sqlite3
from os.path import join as pathjoin
from pathlib import Path

# Like in the server.py file, because I don't know what OS you're using, I have
# to do this path shenanigans. If you were using this for real work, you could
# just use the file path formatted properly for where you're deploying the
# script.
SCHEMA = pathjoin(Path(__file__).parent, "schema.sql")
DATABASE = pathjoin(Path(__file__).parent, "sqlite3.db")

with open(SCHEMA, "r") as file:
    # Read in the script as a string, NOT as lines
    script = file.read()

db = sqlite3.connect(DATABASE)
cursor = db.cursor()
cursor.executescript(script)

# If there is an error, sqlite3 will back out before committing, so we only
# hit this point if the whole script ran successfully.
db.commit()
db.close()
