# Example

This repository is an example of a React frontend and Flask backend which can be
used to serve information from a local database.

## How to Run This Project

### Step 1: Install Python and Virtual Environment `venv`

To run the backend, you must use Python, ideally 3.12 as that is the version I
used to build it. You can install Python using your OS's method; there are many
tutorials for it available by Googling "How to install Python on `{OSName}`".

Then, create a virtual environment or `venv` with which to run the backend. You
can find instructions for how to do that [here]().

NOTE: You **MUST** use the name `venv` for the venv folder or the automated
script in `package.json` won't work properly!

After installing and running the virtual environment, go to the `backend/`
folder and run this command:

```bash
pip install -r requirements.txt
```

(If you are on MacOS, remember to use `pip3` instead of `pip` in this command,
since `pip` is the Python 2 version.)

### Step 2: Run the Project

You can start the backend by going to `backend/` and running

```bash
venv/bin/flask --app server.py --debug run -p 5001
```

To make this easiser, I have defined the command `npm run backend` to do this
for you.

Then, you can run the React frontend project using the standard

```bash
npm run dev
```

## Notes on Syntax

Python syntax is pretty approachable, but there are a couple things to note if
you are unfamiliar with them.

### Decorator Methods

Flask uses 'decorator' methods to set routes and various things. A decorator
begins with `@`, so for example the `@app.route(...)` is a decorator in:

```python
@app.route("/")
def homepage():
    return "<p>This is the root.</p>"
```

Decorators are pure 'syntactic sugar'; they are an abbreviation which makes it
easier to do a repetitive operation. A decorator is a 'higher-order function',
which means that it is a function which takes another function as an argument.

The above decorator is syntactically equivalent to:

```python
def homepage():
    return "<p>This is the root.</p>"
homepage = app.route("/")(homepage)
```

### Dunder Names

Python has a set of reserved names called "dunder" or "double under" names. In
`server.py`, you will see both `__name__` and `__file__`. Under-the-hood, these
are reserved names which are set by the runtime when the script starts running.
The value of `__file__` is the absolute path of the file it appears in; the
value of `__name__` is the name of the file.

Because this project is designed to work on various operating systems, I have
set up the paths to use `Path(__file__).parent` and a built-in path join which
will respect your OS' proper path separator. You can read
`Path(__file__).parent` as "the folder containing the file" it appears in.
