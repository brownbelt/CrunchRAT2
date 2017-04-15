import json
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

# temporarily globally-accessible and hard-coded
with open("pandora_new.json") as data_file:
    data = json.load(data_file)


def beacon():
    resp = make_response()

    # loops through JSON elements and adds in malleable HTTP headers
    for name in data["beacon_response_headers"]:
        resp.headers[name] = data["beacon_response_headers"][name]

    # loops through JSON elements and adds in malleable cookies
    for name in data["beacon_response_cookies"]:
        resp.set_cookie(name, value=data["beacon_response_cookies"][name])

    resp.data = "beacon response"
    return resp


def update():
    resp = make_response()

    # loops through JSON elements and adds in malleable HTTP headers
    for name in data["update_response_headers"]:
        resp.headers[name] = data["update_response_headers"][name]

    # loops through JSON elements and adds in malleable cookies
    for name in data["update_response_cookies"]:
        resp.set_cookie(name, value=data["update_response_cookies"][name])

    resp.data = "update response"
    return resp


if __name__ == "__main__":
    app.add_url_rule(data["implant"]["beacon_uri"], None, beacon, methods=["GET", "POST"])
    app.add_url_rule(data["implant"]["update_uri"], None, update, methods=["GET", "POST"])
    # remove hard-coded port later
    app.run("0.0.0.0", 80)
