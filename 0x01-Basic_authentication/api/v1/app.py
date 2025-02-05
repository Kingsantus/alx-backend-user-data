#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# instancing auth to none
auth = None

# getting AUTH_TYPE from environment
AUTH_TYPE = os.getenv('AUTH_TYPE', None)

# checking the type of AUTH_TYPE gotten
if AUTH_TYPE == 'auth':
    from .auth.auth import Auth
    # instancing auth to Auth
    auth = Auth()

elif auth_type == auth:
    from .auth.auth import BasicAuth

    auth = BasicAuth()


@app.before_request
def before_request_handler():
    """" Handles request before
    """
    if auth is None:
        return

    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/']

    if not auth.require_auth(request.path, excluded_paths):
        return
    else:

        if auth.authorization_header(request) is None:
            abort(401)

        if auth.current_user(request) is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_err(error) -> str:
    """ Unauthorized handler
    Return:
        - error: Unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_err(error) -> str:
    """ Forbidden handler
    Return:
        - error: Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
