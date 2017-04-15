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

    def start_webserver(self):
        if self.protocol == "https":
            # TO DO: add in flask ssl context here instead of print()
            print("https protocol selected")

        # reads json profile
        with open(self.profile) as file:
            json_data = json.load(file)

        # TO DO: check if json_data["implant"]["beacon_uri"] and json_data["implant"]["update_uri"] exist
        # if these do not exist, the user has a malformed json profile

        # TO DO: configure malleable http responses via make_response() here

        # TO DO: inserts entry into "listeners" table

        # adds URIs and starts flask web server
        app.add_url_rule(json_data["implant"]["beacon_uri"], None, self.beacon, methods=["GET", "POST"])
        app.add_url_rule(json_data["implant"]["update_uri"], None, self.update, methods=["GET", "POST"])
        #app.add_url_rule("/beacon", None, self.beacon, methods=["GET", "POST"])
        app.run("0.0.0.0", self.port)

    def beacon(self):
        return "beacon response"

    def update(self):
        return "update response"
