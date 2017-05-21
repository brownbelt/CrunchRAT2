from flask import Flask
from flask import request
from flask import render_template

# creates Flask application instance
app = Flask(__name__)


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


# this is the index "view"
@app.route("/")
def index():
    return "<p>This is the index page.</p>"


# this is the agent "view"
@app.route("/agent")
def agent():
    user_agent = request.headers.get("User-Agent")
    return "<h1>Your User-Agent is %s</h1>" % user_agent


# this is the user "view"
@app.route("/user/<string:name>")
def user(name):
    return "<h1>hello, %s!</h1>" % name


if __name__ == "__main__":
    app.run(debug=True)
