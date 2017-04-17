import json
import pymysql
from core.config import *
from colorama import Fore, Style
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
            j = json.load(file)

        self.app.add_url_rule(j["implant"]["beacon_uri"], None, self.beacon, methods=["GET", "POST"])
        self.app.add_url_rule(j["implant"]["update_uri"], None, self.update, methods=["GET", "POST"])

        # tries to establish a connection to the database
        try:
            self.connection = pymysql.connect(host="localhost", port=3306, user=username, passwd=password, db=database, autocommit=True)

        # exits the program if an exception is raised
        except:
            print(Style.BRIGHT + Fore.RED + "[!] Unable to establish a database connection." + Style.RESET_ALL)
            sys.exit()

    def start_web_server(self):
        try:
            print(Style.BRIGHT + Fore.GREEN + "[+] Starting web server." + Style.RESET_ALL)
            self.app.run("0.0.0.0", self.port)

        # exits the program if an exception is raised
        except:
            print(Style.BRIGHT + Fore.RED + "[!] Error starting web server." + Style.RESET_ALL)
            sys.exit()

    def beacon(self):
        return "beacon response"

    def update(self):
        return "update response"
