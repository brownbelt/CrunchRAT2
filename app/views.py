from flask import render_template
from app import app

@app.route("/", methods=["GET"])
def index():
    return "this is the index page"


@app.route("/test", methods=["GET"])
def test():
    return "this is the test page"


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
