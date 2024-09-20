#!/usr/bin/env python3
""" Module of Index views
"""
from api.v1.views import app_views
from os import getenv
from flask import jsonify, abort, request, make_response


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def new_session() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - the status of the API
    """
    email = request.form.get('email')
    if email is None or not isinstance(email, str) or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or not isinstance(password, str) or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    from models.user import User
    users = User.search({'email': email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = None
    for u in users:
        if u.is_valid_password(password):
            user = u

    if user is None:
        return jsonify({"error": "wrong password"}), 401

    # creating user session form the auth value
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie_name = getenv("SESSION_NAME")
    assert cookie_name is not None

    # setting the session id cookie
    res = make_response(jsonify(user.to_json()))
    res.set_cookie(cookie_name, session_id)

    return res


@app_views.route(
                    '/auth_session/logout',
                    methods=['DELETE'], strict_slashes=False)
def destroy_session() -> str:
    """
    destroy_session: deleting the session for the user
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
