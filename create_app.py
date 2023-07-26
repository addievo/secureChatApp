# create_app.py
from flask import Flask
from flask_session import Session
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    return app
