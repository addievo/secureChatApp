import argparse
import importlib.util
from flask import Flask, url_for
from flask_session import Session
from routes import index, user, chat
from auth.middleware import log_request_info
import ssl
from waitress import serve

# app.py
from create_app import create_app, socketio

app = create_app()
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

parser = argparse.ArgumentParser(description="Run the Flask app")
parser.add_argument('--host', type=str, default='127.0.0.1',
                    help='What host to listen on (default is 127.0.0.1)')
parser.add_argument('--port', type=int, default=5000,
                    help='What port to listen on (default is 5000)')
parser.add_argument('--cert', type=str, default='path_to_your_certificate.pem', help='Path to SSL certificate file')
parser.add_argument('--key', type=str, default='path_to_your_privatekey.pem', help='Path to SSL private key file')


def load_ssl_content(cert_path, key_path):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    return ssl_context


if __name__ == "__main__":
    args = parser.parse_args()
    ssl_context = load_ssl_content(args.cert, args.key)
    serve(app, host=args.host, port=args.port, url_scheme='https', ssl_context=ssl_context)
