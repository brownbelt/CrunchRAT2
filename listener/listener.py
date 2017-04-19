#!/usr/bin/python3

import argparse
import os
import sys
from core.message import Message
from core.webserver import WebServer


def do_arg_checks(args):
    # if invalid protocol
    if args.protocol != "http" and args.protocol != "https":
        Message.display_error('[!] Invalid protocol supplied. Please enter "http" or "https" instead.')
        return False

    # TO DO: checks external address here

    # TO DO: checks port here

    # TO DO: checks json profile here

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
        w = WebServer(args.protocol, args.external_address, args.port, args.profile)

    # exception raised during WebServer class instantiation
    # exits the program
    except Exception as e:
        Message.display_error("[!] Unable to establish database connection.\n" + str(e))
        sys.exit()
