import json
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


class WebServer(object):
    # maybe do json parsing in __init__
    def __init__(self, profile):
        self.profile = profile
        print(self.profile)

    # former beacon.php functionality here
    def beacon(self):
        # parses malleable profile
        with open(self.profile) as data_file:
            data = json.load(data_file)

        # loops through "beacon" json object
        # configures malleable profile (via resp.headers)
        resp = make_response()

        for name in data["beacon"]:
            resp.headers[name] = data["beacon"][name]

        # TO DO: we should actually do parsing here to check if this an initial implant beacon
        resp.data = "beacon response"
        return resp

    def start_webserver(self, port):
        app.add_url_rule("/beacon", None, self.beacon, methods=["GET", "POST"])
        app.run("0.0.0.0", port)
