import logging
import json
from gevent.wsgi import WSGIServer
from flask import Flask, request, redirect, make_response
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.debug = True

@app.errorhandler(404)
def page_not_found(error):
    # TO DO: remove hard-coded redirect
    return redirect("https://www.google.com")

class WebServer(object):

    def __init__(self):
        self.port = 80
        self.profile = "profiles/pandora.json"

        # reads profile as a file
        with open(self.profile) as file:
            self.json_file = json.load(file)


    def test(self):
        return "test"


    def beacon_response(self):
        return "beacon response"


    def start(self):
        print("testing")

        #app.add_url_rule(self.json_file["implant"]["beacon_uri"], None, self.beacon_response, methods=["GET", "POST"])
        app.add_url_rule("/beacon", None, self.beacon_response, methods=["GET", "POST"])


        server = WSGIServer(("0.0.0.0", self.port), app, log=app.logger)
        server.serve_forever()
