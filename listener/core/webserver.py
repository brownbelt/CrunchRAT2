import json
import pymysql
from flask import Flask
from gevent import wsgi
from core.config import *
from core.message import Message


class WebServer(object):

    def __init__(self, args):
        self.protocol = args.protocol
        self.external_address = args.external_address
        self.port = args.port
        self.profile = args.profile

        self.app = Flask(__name__)
        self.app.debug = True

        # tries to establish a connection to the database
        try:
            self.connection = pymysql.connect(
                host="localhost",
                port=3306,
                user=username,
                passwd=password,
                db=database,
                autocommit=True)

        except Exception:
            raise

    def parse_profile_and_route(self):
        try:
            # parses profile
            with open(self.profile) as file:
                j = json.load(file)

                # adds Flask beacon and update routes
                self.app.add_url_rule(j["implant"]["beacon_uri"], None, self.beacon, methods=["GET", "POST"])
                self.app.add_url_rule(j["implant"]["update_uri"], None, self.update, methods=["GET", "POST"])

                # TO DO: add in malleable HTTP responses here

        except Exception:
            raise

    def start_web_server(self):
        # tries to start Flask web server
        try:
            server = wsgi.WSGIServer(("0.0.0.0", self.port), self.app)
            Message.display_status("[+] Successfully started listener on " + self.external_address + ":" + str(self.port))
            server.serve_forever()

            # TO DO: add in INSERT into "listeners" table here

        except KeyboardInterrupt:
            server.stop()

            # TO DO: add in DELETE from "listeners" table here

        except Exception:
            # TO DO: add in DELETE from "listeners" table here

            raise

    def beacon(self):
        return "beacon response"

    def update(self):
        return "update response"
