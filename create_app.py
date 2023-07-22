# create_app.py
from flask import Flask
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    return app
