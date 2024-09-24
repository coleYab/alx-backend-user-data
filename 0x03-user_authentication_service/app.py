#!/usr/bin/env python3
"""
app: creating a simple application terminal
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def homepage() -> str:
    """ get for home page
    """
    return jsonify({"message": "Bienvenue"}), 200

@app.route('/users', methods=['POST'])
def new_users() -> str:
    """ new_users: adds a new user to our db
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
