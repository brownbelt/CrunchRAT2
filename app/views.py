from flask import render_template, redirect
from app import app


@app.route("/", methods=["GET"])
def index():
    return redirect("/login", code=302)


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html"), 200


@app.route("/loginSubmit", methods=["POST"])
def login_submit():
    return "you submitted the login page"
