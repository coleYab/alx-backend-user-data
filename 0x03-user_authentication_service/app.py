#!/usr/bin/env python3
"""
app: creating a simple application terminal
"""
from flask import (
                    Flask, jsonify, request,
                    make_response, abort, redirect
                    )
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


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    profile: method to show user profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({'email': user.email}), 200


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    login: method to manage the user which is in
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie('session_id', session_id)
        return resp

    abort(401)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """
    update_password: updates user password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('new-password')
    try:
        AUTH.update_password(reset_token, password)
        return jsonify({'email': email, 'mesage': 'Password updated'}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    implementaation for getting user reset password token
    """
    try:
        email = request.form.get('email')
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': reset_token})
    except ValueError:
        abort(403)


@app.route('/sessions', methods=['DELETE'])
def logout() -> None:
    """ logging out functionality
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
