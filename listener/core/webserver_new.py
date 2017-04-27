import logging
from gevent.wsgi import WSGIServer
from flask import Flask
from logging.handlers import RotatingFileHandler

# creates flask app
app = Flask(__name__)
app.debug = True

# configures flask logging
# 100 meg maximum file size
log_handler = RotatingFileHandler("../logs/access.log", maxBytes=100000000, backupCount=3)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# starts flask web server
server = WSGIServer(("0.0.0.0", 8000), app, log=app.logger)
server.serve_forever()
