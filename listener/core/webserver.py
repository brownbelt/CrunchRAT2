import json
import pymysql
from flask import Flask
from flask import request
from flask import make_response
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
                self.j = json.load(file)

                # adds Flask beacon and update routes
                self.app.add_url_rule(self.j["implant"]["beacon_uri"], None, self.beacon, methods=["GET", "POST"])
                self.app.add_url_rule(self.j["implant"]["update_uri"], None, self.update, methods=["GET", "POST"])

        except Exception:
            raise

    def start_web_server(self):
        # tries to start Flask web server
        try:
            server = wsgi.WSGIServer(("0.0.0.0", self.port), self.app)

            # add an entry in the "listeners" table
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO `listeners` (`protocol`, `external_address`, `port`, `profile`, `user_agent`, `sleep`, `beacon_uri`, `update_uri`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (self.protocol, self.external_address, self.port, self.profile, self.j["implant"]["user_agent"], self.j["implant"]["sleep"], self.j["implant"]["beacon_uri"], self.j["implant"]["update_uri"]))

            Message.display_status("[+] Successfully started listener on " + self.external_address + ":" + str(self.port))
            server.serve_forever()

        except KeyboardInterrupt:
            pass

        except Exception:
            raise

        finally:
            # deletes entry from "listeners" table
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM `listeners`")

    def beacon(self):
        try:
            resp = make_response()

            # TO DO: loop through profile and add in malleable headers and cookies here

            resp.data = "beacon response"
            return resp

        except Exception:
            raise

    def update(self):
        try:
            resp = make_response()

            # TO DO: loop through profile and add in malleable headers and cookies here

            resp.data = "update response"
            return resp

        except Exception:
            raise
