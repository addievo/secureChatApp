import argparse
import importlib.util
from flask import Flask, url_for
from flask_session import Session
from routes import index, user, chat
from auth.middleware import log_request_info

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
parser.add_argument('--host', type=str, default='192.168.1.91',
                    help='What host to listen on (default is 127.0.0.1)')
parser.add_argument('--port', type=int, default=5201,
                    help='What port to listen on (default is 5000)')

if __name__ == "__main__":
    args = parser.parse_args()
    socketio.run(app, host=args.host, port=args.port, debug=False, use_reloader=False)
