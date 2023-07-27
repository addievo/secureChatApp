from functools import wraps

from flask import session, request, redirect, url_for, current_app



def log_request_info():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())



def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index.login'))
        return f(*args, **kwargs)
    return decorated_function