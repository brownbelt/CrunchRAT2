#!/usr/bin/python3

import argparse
import ipaddress
import json
import os
import socket
import sys
from core.message import Message
from core.webserver import WebServer


def do_arg_checks(args):
    # checks protocol
    if args.protocol != "http" and args.protocol != "https":
        Message.display_error('[!] Invalid protocol. Please enter "http" or "https" instead.')
        return False

    # checks external address
    try:
        ipaddress.ip_address(args.external_address)

    except Exception as e:
        Message.display_error("[!] Invalid external address.\n" + str(e))
        return False

    # checks port here
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", args.port))

    except OverflowError as e:
        Message.display_error("[!] Invalid port supplied. Please choose a port between 1-65535.\n" + str(e))
        return False

    except socket.error as e:
        Message.display_error("[!] Port already in use. Please choose another port.\n" + str(e))
        return False

    # checks json profile here
    try:
        with open(args.profile) as file:
            j = json.load(file)

            # if "beacon_uri" property does not exist in profile
            if "beacon_uri" not in j["implant"]:
                Message.display_error('[!] Profile must contain a "beacon_uri" property.')
                return False

            # if "update_uri" property does not exist in profile
            if "update_uri" not in j["implant"]:
                Message.display_error('[!] Profile must contain a "update_uri" property.')
                return False

            # if "sleep" property does not exist in profile
            if "sleep" not in j["implant"]:
                Message.display_error('[!] Profile must contain a "sleep" property.')
                return False

            # if "user_agent" property does not exist in profile
            if "user_agent" not in j["implant"]:
                Message.display_error('[!] Profile must contain a "user_agent" property.')
                return False

    except Exception as e:
        Message.display_error("[!] Invalid profile supplied. Please make sure the profile is a valid JSON file.\n" + str(e))
        return False

    # all checks passed at this point
    return True


if __name__ == "__main__":
    # if not ran with sudo or root privileges
    # exits the program
    if os.geteuid() != 0:
        Message.display_error("[!] Please re-run with sudo or root privileges.")
        sys.exit()

    parser = argparse.ArgumentParser(prog="listener.py", description="CrunchRAT2 Listener - Written by Hunter Hardman @t3ntman")
    parser.add_argument("protocol", action="store", type=str, help="listener protocol [http][https]")
    parser.add_argument("external_address", action="store", type=str, help="listener external address")
    parser.add_argument("port", action="store", type=int, help="listener port")
    parser.add_argument("profile", action="store", type=str, help="listener profile")

    # parses command-line arguments
    args = parser.parse_args()

    # checks command-line arguments for issues
    # exits the program if any issues
    if do_arg_checks(args) is not True:
        sys.exit()

    # tries to instantiate WebServer class
    try:
        w = WebServer(args)

    # exception raised during WebServer class instantiation
    # exits the program
    except Exception as e:
        Message.display_error("[!] Unable to establish database connection.\n" + str(e))
        sys.exit()
