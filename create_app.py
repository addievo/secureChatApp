# create_app.py
from flask import Flask, request
from flask_session import Session
from flask_cors import CORS
from flask_socketio import SocketIO


socketio = SocketIO() # declare socketio object globally



def create_app():
    app = Flask(__name__)
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    socketio.init_app(app, cors_allowed_origins="https://chat.adityav.au")
    return app