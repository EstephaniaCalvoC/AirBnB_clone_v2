#!/usr/bin/python3
"""Start a Flask web application
- listening on 0.0.0.0, port 5000
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Display “Hello HBNB!”"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display “HBNB”"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def cText(text):
    """Display “C ” followed by <text> variable"""
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
