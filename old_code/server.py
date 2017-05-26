import argparse
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask_bcrypt import Bcrypt
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

bcrypt = Bcrypt(app)

# SQLAlchemy configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "rat.db")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# creates Flask-Login instance
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)


class User(db.Model):
    # creates SQLite "users" table
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(255))

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

    # TO DO: check if valid credentials
    # OBVIOUSLY THIS WON'T BE HARDCODED
    # WE NEED TO QUERY THE FIRST FIELD FROM THE "users" TABLE
    # THEN CROSS-REF IT AGAINST THE SECOND ARG (THE TYPED IN PASSWORD)
    print(bcrypt.check_password_hash("$2b$12$6YgIwJR56oQqXNTg/3f0punBzsk6CyYMFlUkVRkvLh20KWrCa8LJK", password))

    if bcrypt.check_password_hash("$2b$12$6YgIwJR56oQqXNTg/3f0punBzsk6CyYMFlUkVRkvLh20KWrCa8LJK", password) == True:
        return "successful authentication"

    else:
        return "failed authentication"

    # generates password hash using bcrypt
    #password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    #user = User(username=username, password_hash=password_hash)
    #db.session.add(user)
    #login_user("hunter")


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

    # THIS CODE WILL NEED MOVED SOMEWHERE ELSE
    #pw_hash = bcrypt.generate_password_hash('hunter2').decode("utf-8")
    #print(bcrypt.check_password_hash(pw_hash, 'hunter2')) # returns True
    #print(bcrypt.check_password_hash(pw_hash, 'hunter3')) # returns False

    # starts Flask listener
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()
