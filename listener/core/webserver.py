import base64
import datetime
import logging
import json
import random
import sqlite3
import string
from config import *
from message import *
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

    def start_flask_server(self, protocol, external_address, port, profile):
        # tries to start the Flask web server
        try:
            # reads profile as a file
            with open(profile) as file:
                j = json.load(file)

            # configures Flask logging with 100 meg max file size
            # all requests are logged to "listener/logs/access.log"
            log_handler = RotatingFileHandler("../logs/access.log", maxBytes=100000000, backupCount=3)
            app.logger.addHandler(log_handler)
            app.logger.setLevel(logging.INFO)

            # INSERTS an entry into the "listener" table
            # CREATE TABLE listeners (protocol TEXT, external_address TEXT, port TEXT, profile TEXT);
            # ** ONLY INCLUDE THE COLUMNS ABOVE - SHOULD HAVE FUNCTION CALLED insert_into_listeners() **

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

        # finally closes sqlite connection opened in __init__()
        finally:
            self.connection.close()

# END OF CLASS
# DEBUGGING BELOW
w = WebServer()
w.start_flask_server("http", "192.168.1.1", 8080, "../profiles/pandora.json")
