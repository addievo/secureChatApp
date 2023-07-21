# from database.database import get_user, create_user
# from encryption.key_generation import generate_key_pair
# from flask import Flask, request, session, Limiter
# from werkzeug.security import generate_password_hash, check_password_hash
# from app import app
#
#
# def get_remote_address():
#     return request.remote_addr
#
#
# limiter = Limiter(app, key_func=get_remote_address)
#
#
# @limiter.limit('5 per minute')
# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.form['username']
#     password = request.form['password']
#     private_key, public_key = generate_key_pair()
#
#     # hashing the password
#
#     password_hash = generate_password_hash(password)
#     create_user(username, password_hash, public_key, private_key)
#
#     return 'User successfully created', 201
#
#
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#
#     user = get_user(username)
#
#     if user is not None and check_password_hash(user.password_hash, password):
#         session['username'] = username
#         return 'Logged in successful', 200
#     else:
#         return 'Invalid username or password', 401
#
#
# @app.route('/logout', methods=['POST'])
# def logout():
#     session.pop('username', None)
#     return 'Logged out successfully', 200
