from flask import Flask, Limiter, render_template, redirect, url_for, request, session
from database.database import get_user, create_user
from encryption.key_generation import generate_key_pair
from werkzeug.security import generate_password_hash, check_password_hash
from app import app


def get_remote_address():
    return request.remote_addr


limiter = Limiter(app, key_func=get_remote_address)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('chat.html')
    else:
        return redirect(url_for('login'))

@app.route('signup', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def signup():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        private_key, public_key = generate_key_pair()

        #hashing the password

        password_hash = generate_password_hash(password)
        create_user(username, password_hash, public_key, private_key)

        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)

        if user is not None and check_password_hash(user.password_hash, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password', 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return 'Logged out successfully', 200
