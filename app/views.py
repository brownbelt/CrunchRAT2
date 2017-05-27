from flask import render_template
from app import app


@app.route("/", methods=["GET"])
def index():
    return "index page here"


@app.route("/login", methods=["GET"])
def login():
    return "login page here"
