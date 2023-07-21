from flask import request, Flask, Limiter, session
from app import app


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())




@app.errorhandler(500)
def handle_internal_error():
    return 'Internal Server Error', 500


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return 'Unauthorised', 401
