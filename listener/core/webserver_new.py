import base64
import json
import logging
from gevent.wsgi import WSGIServer
from flask import Flask, request, redirect
from logging.handlers import RotatingFileHandler

# creates Flask app
app = Flask(__name__)
app.debug = True

# beacon route
# TO DO: remove hard-coded beacon URI
def beacon_response():
    return "beacon response"

# update route
# TO DO: remove hard-coded update URI
def update_response():
    return "update response"
