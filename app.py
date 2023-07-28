import argparse
import importlib.util
from flask import Flask, url_for
from flask_session import Session
from routes import index, user, chat
from auth.middleware import log_request_info
from flask_cors import CORS

# app.py
from create_app import create_app, socketio

app = create_app()
cors = CORS(app, resources={r"/*": {"origins": "https://chat.adityav.au"}})

app.register_blueprint(index.bp)
app.register_blueprint(user.bp)
app.register_blueprint(chat.bp)
app.before_request(log_request_info)
#error handling
@app.errorhandler(500)
def handle_internal_error(error):
    return 'Internal server error', 500

@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    return "<br>".join(output)

# Load routes/index.py using importlib
spec = importlib.util.spec_from_file_location("index", "./routes/index.py")
index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index)

print("Starting server...")

if __name__ == "__main__":
    print("Inside main...")
    socketio.run(app, host='192.168.1.90', port='5201')
    print("Server started.")
