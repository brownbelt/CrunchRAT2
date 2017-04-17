import pymysql
from core.config import *
from colorama import Fore, Style
from flask import Flask
from flask import request


class WebServer(object):
    def __init__(self, protocol, external_address, port):
        self.protocol = protocol
        self.external_address = external_address
        self.port = port

        self.app = Flask(__name__)

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
