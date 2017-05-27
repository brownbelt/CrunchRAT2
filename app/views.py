from flask import render_template
from app import app


@app.route("/", methods=["GET"])
def index():
    return "index page here"


@app.route("/login", methods=["GET"])
def login():
    return "login page here"


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
