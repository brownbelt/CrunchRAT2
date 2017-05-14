import base64
import datetime
import logging
import json
import random
import sqlite3
import string
from core.config import *
from core.message import *
from gevent.wsgi import WSGIServer
from flask import Flask, request, redirect
from logging.handlers import RotatingFileHandler

# creates Flask app
app = Flask(__name__)
app.debug = True


class WebServer(object):

    def __init__(self):
        # tries to open sqlite connection
        try:
            # uses database path specified in "config.py"
            self.connection = sqlite3.connect(database_path)

        # exception raised during sqlite connection
        except Exception:
            raise

    def is_base64(self, string):
        """
        DESCRIPTION:
            This function checks if a specified string is Base64 encoded or not
        """
        # tries to Base64 decode
        try:
            base64.b64decode(string).decode()
            return True

        # exception raised during Base64 decode
        except Exception:
            return False

    def beacon_response(self):
        """
        DESCRIPTION:
            This function is called when an implant beacons
        """
        # gets raw POST data
        raw_data = request.get_data()

        # if initial Base64 beacon
        # new beacon
        if self.is_base64(raw_data) is True:
            return "Base64 beacon"

        # else RC4-encrypted beacon
        else:
            return "RC4 beacon"

    def start_flask_server(self, protocol, external_address, port, profile):
        """
        DESCRIPTION:
            This function starts the Flask web server
        """
        # tries to start the Flask web server
        try:
            # reads profile as a file
            with open(profile) as file:
                j = json.load(file)

            # adds beacon route for Flask
            app.add_url_rule(j["implant"]["beacon_uri"],
                             None,
                             self.beacon_response,
                             methods=["POST"])

            # configures Flask logging with 100 meg max file size
            # all requests are logged to "listener/logs/access.log"
            log_handler = RotatingFileHandler("logs/access.log",
                                              maxBytes=100000000,
                                              backupCount=3)
            app.logger.addHandler(log_handler)
            app.logger.setLevel(logging.INFO)

            # INSERTS an entry into the "listeners" table
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO listeners VALUES (?,?,?,?)",
                               (protocol,
                                external_address,
                                port,
                                profile))

            # starts Flask web server
            server = WSGIServer(("0.0.0.0", port), app, log=app.logger)
            print_status("[+] Started listener on tcp/" + str(port))
            server.serve_forever()

        # ignores KeyboardInterrupt exception
        except KeyboardInterrupt:
            pass

        # exception raised starting the Flask web server
        except Exception:
            raise

        # finally deletes all entries from "listeners" table
        # and closes sqlite connection opened in __init__()
        finally:
            # deletes all entries from "listeners" table
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM listeners")

            # closes sqlite connection
            self.connection.close()
