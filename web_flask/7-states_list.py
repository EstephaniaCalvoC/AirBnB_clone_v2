#!/usr/bin/python3
"""Start a Flask web application
- listening on 0.0.0.0, port 5000
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exc):
    """Close SQLAlchemy session."""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Display an HTML page
    - H1: “States”
    - UL: with the list of all State
    - LI: <state.id>: <B><state.name></B>
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
