import json
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


class WebServer(object):
    def __init__(self, protocol, external_address, port, profile):
        self.protocol = protocol
        self.external_address = external_address
        self.profile = profile
        self.port = port
        self.profile = profile

        # reads json profile
        with open(self.profile) as file:
            self.json_data = json.load(file)

    def start_webserver(self):
        if self.protocol == "https":
            # TO DO: add in flask ssl context here instead of print()
            print("https protocol selected")

        # TO DO: inserts entry into "listeners" table

        # adds routes and starts flask web server
        app.add_url_rule(self.json_data["implant"]["beacon_uri"], None, self.beacon, methods=["GET", "POST"])
        app.add_url_rule(self.json_data["implant"]["update_uri"], None, self.update, methods=["GET", "POST"])
        app.run("0.0.0.0", self.port)

    def beacon(self):
        # parses json profile and configures malleable beacon http response
        self.resp = make_response()
        self.resp.data = "beacon response"
        return self.resp


    def update(self):
        # parses json profile and configures malleable beacon http response
        self.resp = make_response()
        self.resp.data = "update response"
        return self.resp
