from functools import wraps

from flask import session, request, redirect, url_for

from app import app


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.errorhandler(500)
def handle_internal_error():
    return 'Internal Server Error', 500


@app.before_request
def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function