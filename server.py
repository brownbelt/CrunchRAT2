import argparse
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# creates Flask application instance
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "rat.db")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# creates Flask-Login instance
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return "<User %r>" % self.username


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


# redirects all HTTP GET / requests to /login
@app.route("/", methods=["GET"])
def index():
    return redirect("/login", 302)


# Login page
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html"), 200


# Login form submit function
@app.route("/loginSubmit", methods=["POST"])
def login_submit():
    username = request.form["username"]
    password = request.form["password"]

    user = User(username=username)
    db.session.add(user)

    #login_user("hunter")
    return "boop"


@app.route("/home")
@login_required
def home():
    pass





if __name__ == "__main__":
    # creates SQLite database and tables
    db.create_all()

    # argument configuration and parsing
    parser = argparse.ArgumentParser(prog="server.py",
                                     description="CrunchRAT v2.0")
    parser.add_argument("password",
                        action="store",
                        type=str,
                        help="server password")

    args = parser.parse_args()

    # starts Flask listener
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()
