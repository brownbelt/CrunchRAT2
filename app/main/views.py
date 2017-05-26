from flask import render_template
#from . import app


@app.route("/test")
def test():
    return "this is a test page"
