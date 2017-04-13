from flask import Flask

app = Flask(__name__)


class WebServer(object):
    def __init__(self):
        # DEBUGGING - WILL REMOVE LATER
        print("test")

    def start_webserver(self, port):
        app.run("0.0.0.0", port)
