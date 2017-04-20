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

    def start_web_server(self):
        # tries to start Flask web server
        try:
            server = wsgi.WSGIServer(("0.0.0.0", self.port), self.app)
            Message.display_status("[+] Successfully started web server on " + self.external_address + ":" + str(self.port))
            server.serve_forever()

        except KeyboardInterrupt:
            server.stop()

        except Exception:
            raise
