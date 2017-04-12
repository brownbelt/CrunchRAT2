import json
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


def beacon():
    # malleable C2 profile here - DEBUGGING
    with open("profiles/pandora.json") as data_file:
        data = json.load(data_file)
    
    resp = make_response()
    resp.headers["Host"] = data["beacon"]["host"]
    resp.headers["Referer"] = data["beacon"]["referer"]
    resp.headers["Accept"] = data["beacon"]["accept"]
    resp.headers["Accept-Language"] = data["beacon"]["accept-language"]
    resp.headers["Content-Type"] = data["beacon"]["content-type"]
    resp.headers["Server"] = "Apache"

    return resp


if __name__ == "__main__":
    with open("profiles/pandora.json") as data_file:
        data = json.load(data_file)
        beacon_uri = data["beacon"]["uri"]

    app.add_url_rule(beacon_uri, None, beacon, methods=["GET", "POST"])

    # 0.0.0.0 makes the server publicly-accessible
    app.run("0.0.0.0", 80)
