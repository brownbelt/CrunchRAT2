import base64
import json
import pymysql
import sys
from core.config import *
from core.tasking import Tasking
from colorama import Fore, Style
from gevent import wsgi
from flask import Flask


class WebServer(object):
    def __init__(self, protocol, external_address, port, profile):
        self.protocol = protocol
        self.external_address = external_address
        self.port = port
        self.profile = profile

        self.app = Flask(__name__)

        # parses json profile and gets "beacon_uri" and "update_uri"
        with open(self.profile) as file:
            self.j = json.load(file)

        self.app.add_url_rule(self.j["implant"]["beacon_uri"], None, self.beacon, methods=["GET", "POST"])
        self.app.add_url_rule(self.j["implant"]["update_uri"], None, self.update, methods=["GET", "POST"])

        # tries to establish a connection to the database
        try:
            self.connection = pymysql.connect(host="localhost", port=3306, user=username, passwd=password, db=database, autocommit=True)

        # exits the program if an exception is raised
        except:
            print(Style.BRIGHT + Fore.RED + "[!] Unable to establish a database connection." + Style.RESET_ALL)
            sys.exit()

    def start_web_server(self):
        # inserts an entry into the "listeners" table
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO `listeners` (`protocol`, `external_address`, `port`, `profile`, `user_agent`, `sleep`, `beacon_uri`, `update_uri`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (self.protocol, self.external_address, self.port, self.profile, self.j["implant"]["user_agent"], self.j["implant"]["sleep"], self.j["implant"]["beacon_uri"], self.j["implant"]["update_uri"]))

        try:
            print(Style.BRIGHT + Fore.GREEN + "[+] Starting listener..." + Style.RESET_ALL)
            server = wsgi.WSGIServer(("0.0.0.0", self.port), self.app)
            server.serve_forever()

        except KeyboardInterrupt:
            pass

        # exits the program if an exception is raised
        except:
            print(Style.BRIGHT + Fore.RED + "[!] Error starting web server." + Style.RESET_ALL)
            sys.exit()

        # web server is killed at this point
        # we remove the entry from the "listeners" table
        finally:
            print(Style.BRIGHT + Fore.GREEN + "[+] Stopping listener..." + Style.RESET_ALL)

            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM `listeners`")

            sys.exit()

    def beacon(self):
        '''
            Description: This is the function called when an implant beacons
        '''
        return "beacon response"


    def update(self):
        '''
            Description: This is the function called when an implant updates
        '''
        return "update response"
