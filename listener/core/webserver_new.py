import logging
import json
from gevent.wsgi import WSGIServer
from flask import Flask, request, redirect
from logging.handlers import RotatingFileHandler

# creates Flask app
app = Flask(__name__)
app.debug = True



@app.route("/<path:path>")
def catch_all(path):
    return redirect(app.config["redirect_url"])


def beacon_response():
    return "beacon response"



def start_flask(protocol, port, profile):
    app.config["protocol"] = protocol
    app.config["port"] = port
    app.config["profile"] = profile

    # reads profile as a file
    with open(profile) as file:
        j = json.load(file)

    app.config["redirect_url"] = j["implant"]["redirect_url"]

    app.add_url_rule("/beacon", None, beacon_response, methods=["GET", "POST"])


    log_handler = RotatingFileHandler("logs/access.log", maxBytes=100000000, backupCount=3)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    server = WSGIServer(("0.0.0.0", port), app, log=app.logger)
    server.serve_forever()
