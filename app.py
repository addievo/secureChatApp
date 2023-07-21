from flask import Flask
from flask_session import Session


app = Flask(__name__)

#configuring the session

app.config['SESSION_PERMANENT']=False
app.config['SESSION_TYPE']='filesystem'
Session(app)

#Import the routes

from routes import index, chat, user

if __name__ == '__main__':
    app.run(debug=True)