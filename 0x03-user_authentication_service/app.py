#!/usr/bin/env python3
"""
app: creating a simple application terminal
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def homepage() -> str:
    """ get for home page
    """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
