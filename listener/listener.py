import argparse
import ipaddress
import json
import socket
import sys
from colorama import Fore, Style
from flask import Flask

# DEBUGGING
from core.server import Server

app = Flask(__name__)


if __name__ == "__main__":
    # TO DO: add in checks for python 2.x

    # TO DO: add in sudo checks

    # parses arguments
    parser = argparse.ArgumentParser(prog="listener.py", description="CrunchRAT2 Listener - Written by Hunter Hardman @t3ntman")
    parser.add_argument("protocol", nargs="?", type=str, help="listener protocol [http][https]")
    parser.add_argument("external_address", nargs="?", type=str, help="listener external address")
    parser.add_argument("port", nargs="?", type=int, help="listener port")
    parser.add_argument("profile", nargs="?", type=argparse.FileType("r"), help="json profile")
    args = parser.parse_args()

    # saves provided arguments
    protocol = args.protocol
    external_address = args.external_address
    port = args.port
    profile = args.profile

    # if protocol is not "http" or "https"
    # prints error and exits the program
    if protocol != "http" and protocol != "https":
        print(Style.BRIGHT + Fore.RED + '[!] Invalid protocol supplied. Please enter "http" or "https".' + Style.RESET_ALL)
        sys.exit(0)

    # TO DO: add in check for "https" so we can add in the flask ssl context

    # checks if supplied address is valid
    try:
        ipaddress.ip_address(external_address)

    # exception raised means invalid external address was provided
    # prints error and exits the program
    except:
        print(Style.BRIGHT + Fore.RED + "[!] Invalid external address supplied." + Style.RESET_ALL)
        sys.exit(0)

    # checks if port is available
    # prints error message and exits if the port is in use
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.connect(("localhost", port))
        print(Style.BRIGHT + Fore.RED + "[!] Port already in use. Please choose another port." + Style.RESET_ALL)
        sys.exit(0)

    except:
        pass

    # tries to load and parse the json profile
    # exception raised means an invalid json profile was provided
    try:
        with open("profiles/pandora.json") as data_file:
            profile_json = json.load(profile)

            # DEBUGGING - NOT SOLD ON THE VARIABLE NAME ABOVE
            print(profile_json)

    # prints error and exits the program
    except:
        print(Style.BRIGHT + Fore.RED + "[!] Error parsing the provided JSON profile." + Style.RESET_ALL)
        sys.exit(0)

    # all arguments have been validated at this point

    # DEBUGGING
    s = Server()
    s.beacon()
    s.update()

    # TO DO: INSERT entry into "listeners" table

    # TO DO: start flask listener
    #app.run("0.0.0.0", port)
