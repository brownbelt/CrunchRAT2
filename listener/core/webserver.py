import json
import pymysql
import sys
from core.config import *
from colorama import Fore, Style
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


class WebServer(object):
    def __init__(self, protocol, external_address, port, profile):
        self.protocol = protocol
        self.external_address = external_address
        self.profile = profile
        self.port = port
        self.profile = profile

        # reads json profile
        with open(self.profile) as file:
            self.json_data = json.load(file)

        # tries to establish a connection to the database
        try:
            self.connection = pymysql.connect(host="localhost", port=3306, user=username, passwd=password, db=database, autocommit=True)

        # exits the program if an exception is raised
        except:
            print(Style.BRIGHT + Fore.RED + "[!] Unable to establish database connection." + Style.RESET_ALL)
            sys.exit()

    def start_webserver(self):
        if self.protocol == "https":
            # TO DO: add in flask ssl context here instead of print()
            print("https protocol selected")

        # inserts entry into "listeners" table
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO listeners (protocol, external_address, port, profile) VALUES (%s, %s, %s, %s)",
            (self.protocol, self.external_address, self.port, self.profile))
        cursor.close()

        # TO DO: wrap this in a try except statement

        # adds routes and starts flask web server
        app.add_url_rule(self.json_data["implant"]["beacon_uri"], None, self.beacon, methods=["GET", "POST"])
        app.add_url_rule(self.json_data["implant"]["update_uri"], None, self.update, methods=["GET", "POST"])
        app.run("0.0.0.0", self.port)

    def stop_webserver(self):
        # TO DO: stop flask webserver
        # this will be called if a keyboard exception (CTRL+C) is raised

        # TO DO: delete entry from "listeners" table
        print("stopping webserver") # DEBUGGING

    def beacon(self):
        # parses json profile and configures malleable beacon http response
        self.resp = make_response()
        self.resp.data = "beacon response"
        return self.resp


    def update(self):
        # parses json profile and configures malleable update http response
        self.resp = make_response()
        self.resp.data = "update response"
        return self.resp
