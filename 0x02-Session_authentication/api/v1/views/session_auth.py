#!/usr/bin/env python3
"""session_auth handles all routes for the session authentication"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import environ


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False)
def login():
    """handles the login for user"""

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(environ.get('SESSION_NAME'), session_id)


@app_views.route(
        '/auth_session/logout/',
        methods=['DELETE'],
        strict_slashes=False)
def logout():
    """logout user"""

    from api.v1.app import auth
    session_id = auth.destroy_session(request)

    if not session_id:
        abort(404)

    return jsonify({}), 200
