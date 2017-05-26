from flask import Blueprint
from flask import render_template

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return "main"


# HTTP 403 route
@main.app_errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


# HTTP 404 route
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# HTTP 500 route
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
