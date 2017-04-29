import logging
import json
from gevent.wsgi import WSGIServer
from flask import Flask, request, redirect
from logging.handlers import RotatingFileHandler

# creates Flask app
app = Flask(__name__)
app.debug = True

@app.errorhandler(404)
def page_not_found(error):
    """
    DESCRIPTION:
        This function redirects all 404 requests to "redirect_url"
    """
    return redirect(app.config["redirect_url"])

@app.route("/<path:path>")
def catch_all(path):
    """
    DESCRIPTION:
        This function redirects all other requests to "redirect_url"
    """
    return redirect(app.config["redirect_url"])





class WebServer(object):
    def __init__(self, args):
        self.protocol = args.protocol
        self.external_address = args.external_address
        self.port = args.port
        self.profile = args.profile

    def beacon_response(self):
        return "beacon response"

    def start_flask(self):
        app.config["protocol"] = self.protocol
        app.config["port"] = self.port
        app.config["profile"] = self.profile

        # reads profile as a file
        with open(self.profile) as file:
            j = json.load(file)

        app.config["redirect_url"] = j["implant"]["redirect_url"]

        app.add_url_rule("/beacon", None, self.beacon_response, methods=["GET", "POST"])

        server = WSGIServer(("0.0.0.0", self.port), app, log=app.logger)
        server.serve_forever()
