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
    from api.v1.auth.auth import Auth
    # instancing auth to Auth
    auth = Auth()

elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.auth import BasicAuth
    # instancing auth to BasicAuth
    auth = BasicAuth()

elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    # instancing auth to SessionAuth
    auth = SessionAuth()

elif AUTH_TYPE == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    # instancing auth to SessionExpAuth
    auth = SessionExpAuth()

elif AUTH_TYPE == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    # instancing auth to SessionExpAuth
    auth = SessionDBAuth()


@app.before_request
def before_request_handler():
    """" Handles request before
    """
    if auth is None:
        return

    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    else:

        if not auth.authorization_header(request) and \
                not auth.session_cookie(request):
            abort(401)

        if auth.current_user(request) is None:
            abort(403)
        request.current_user = auth.current_user(request)


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
