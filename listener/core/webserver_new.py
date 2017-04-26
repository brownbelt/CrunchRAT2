import logging
from gevent.wsgi import WSGIServer
from flask import Flask
from logging.handlers import RotatingFileHandler

# creates flask app
app = Flask(__name__)
app.debug = True

# configures flask logging
log_handler = RotatingFileHandler("access.log", maxBytes=1000000, backupCount=1)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# starts flask web server
server = WSGIServer(("0.0.0.0", 8000), app, log=app.logger)
server.serve_forever()
