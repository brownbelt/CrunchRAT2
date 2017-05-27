from flask import render_template
from app import app


@app.route("/", methods=["GET"])
def index():
    return "index page here"


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html"), 200


@app.route("/loginSubmit", methods=["POST"])
def login_submit():
    return "you submitted the login page"
