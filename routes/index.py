from flask import Blueprint, render_template, redirect, url_for, request, session
from database.database import get_user, create_user
from encryption.key_generation import generate_key_pair
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
def get_remote_address():
    return request.remote_addr


bp = Blueprint('index', __name__, url_prefix='/')
limiter = Limiter(key_func=get_remote_address)

# Define your routes as before, but replace @app.route with @bp.route

@bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'OK', 200

@bp.route('/')
def index():

    if 'username' in session:
        username = get_user(session['username']).username
        return render_template('chat.html',username=username)
    else:
        return render_template('index.html')


@bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit('50 per minute')
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        private_key, public_key = generate_key_pair()

        # hashing the password
        #check if user exists
        if get_user(username):
            return render_template('signup.html', error="Username is already taken.")

        password_hash = generate_password_hash(password)
        create_user(username, password_hash, public_key, private_key)

        return redirect(url_for('index.login'))
    else:
        return render_template('signup.html')



@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('50 per minute')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)

        if user is None:
            # User does not exist
            return render_template('login.html', error="Username does not exist."), 401
        elif not check_password_hash(user.password_hash, password):
            # Password is incorrect
            return render_template('login.html', error="Password is incorrect."), 401
        else:
            session['username'] = username
            return redirect(url_for('index.index'))  # Redirect to index after successful login
    else:
        return render_template('login.html')



@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return render_template('index.html')
