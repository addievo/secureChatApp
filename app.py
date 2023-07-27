import argparse
import importlib.util
from flask import Flask, url_for
from flask_session import Session
from routes import index, user, chat
from auth.middleware import log_request_info
import ssl
from waitress import serve
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

cert_path = 'certificate.pem'
key_path = 'privatekey.pem'
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)



if __name__ == "__main__":
    socketio.run(app, host='192.168.1.90', port='5201', ssl_context=ssl_context)
