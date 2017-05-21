import argparse
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from gevent.wsgi import WSGIServer
import os


# creates Flask application instance
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)


# HTTP 403
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


# HTTP 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# HTTP 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# Login page
@app.route("/login")
def login():
    return render_template("login.html"), 200


# Login form submit function
@app.route("/loginSubmit", methods=["POST"])
def login_submit():
    password = request.form["password"]

    if password == args.password:
        return "successful authentication"

    else:
        return "failed authentication"


# this is the index "view"
@app.route("/")
def index():
    return "<p>This is the index page.</p>"


# this is the user "view"
@app.route("/user/<string:name>")
def user(name):
    return "<h1>hello, %s!</h1>" % name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server.py",
                                     description="CrunchRAT v2.0")
    parser.add_argument("password",
                        action="store",
                        type=str,
                        help="server password")

    # parses command-line arguments
    args = parser.parse_args()

    # starts Flask listener
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()
