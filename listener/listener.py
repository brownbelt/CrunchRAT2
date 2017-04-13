import argparse
import ipaddress
import json
import socket
import sys
from colorama import Fore, Style
from flask import Flask
from core.argchecks import ArgChecks

app = Flask(__name__)


if __name__ == "__main__":
    # TO DO: add in checks for python 2.x

    # TO DO: add in sudo checks

    # parses arguments
    parser = argparse.ArgumentParser(prog="listener.py", description="CrunchRAT2 Listener - Written by Hunter Hardman @t3ntman")
    parser.add_argument("protocol", nargs="?", type=str, help="listener protocol [http][https]")
    parser.add_argument("external_address", nargs="?", type=str, help="listener external address")
    parser.add_argument("port", nargs="?", type=int, help="listener port")
    #parser.add_argument("profile", nargs="?", type=argparse.FileType("r"), help="json profile")
    parser.add_argument("profile", nargs="?", type=str, help="json profile")
    args = parser.parse_args()

    # performs argument checks
    c = ArgChecks()
    c.protocol_check(args.protocol)
    c.external_address_check(args.external_address)
    c.port_check(args.port)
    c.profile_check(args.profile)
