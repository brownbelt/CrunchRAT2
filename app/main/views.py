from flask import render_template, session, redirect, url_for
from . import main

@main.route("/", methods =["GET"]
def index():
    return "index page here"
