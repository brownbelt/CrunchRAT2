import logging
import pymysql
from core.config import *
from gevent.wsgi import WSGIServer
from flask import Flask
from logging.handlers import RotatingFileHandler


class WebServer(object):

    def __init__(self, args):
        # we will reference these variables throughout the class
        self.protocol = args.protocol
        self.external_address = args.external_address
        self.port = args.port
        self.profile = args.profile

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

    def start_web_server(self, port):
        """
        DESCRIPTION:
            This function creates and starts the Flask web server

        RETURNS:
            None
        """
        # tries to create and start the Flask web server
        try:
            # creates Flask app
            app = Flask(__name__)
            app.debug = True

            # configures Flask logging with 100 meg max file size
            # all requests are logged to "listener/logs/access.log"
            log_handler = RotatingFileHandler("logs/access.log", maxBytes=100000000, backupCount=3)
            app.logger.addHandler(log_handler)
            app.logger.setLevel(logging.INFO)

            # starts Flask web server
            server = WSGIServer(("0.0.0.0", port), app, log=app.logger)
            server.serve_forever()

        # exception raised creating and starting the Flask web server
        except Exception:
            raise
