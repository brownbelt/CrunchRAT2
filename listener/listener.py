#!/usr/bin/python3

import argparse
import os
import sys
from colorama import Fore, Style
from core.argchecks import ArgChecks


if __name__ == "__main__":
    # if not ran with sudo or root privileges
    # exits the program
    if os.geteuid() != 0:
        print(Style.BRIGHT + Fore.RED + "[!] Please re-run with sudo or root privileges." + Style.RESET_ALL)
        sys.exit()

    # parses arguments
    parser = argparse.ArgumentParser(prog="listener.py", description="CrunchRAT2 Listener - Written by Hunter Hardman @t3ntman")
    parser.add_argument("protocol", nargs="?", type=str, help="listener protocol [http][https]")
    parser.add_argument("external_address", nargs="?", type=str, help="listener external address")
    parser.add_argument("port", nargs="?", type=int, help="listener port")
    parser.add_argument("profile", nargs="?", type=str, help="json profile")
    args = parser.parse_args()

    # performs argument checks
    c = ArgChecks()
    c.protocol_check(args.protocol)
    c.external_address_check(args.external_address)
    c.port_check(args.port)
    c.profile_check(args.profile)
