#!/usr/bin/python3

import argparse
import json
import os
import pymysql
import sys
from colorama import Fore, Style
from core.config import *


if __name__ == "__main__":
    # if not ran with sudo or root privileges
    # exits the program
    if os.geteuid() != 0:
        print(Style.BRIGHT + Fore.RED + "[!] Please re-run with sudo or root privileges." + Style.RESET_ALL)
        sys.exit()

    # parses arguments
    parser = argparse.ArgumentParser(prog="listener.py", description="CrunchRAT2 Listener - Written by Hunter Hardman @t3ntman")
    parser.add_argument("protocol", action="store", type=str, help="listener protocol [http][https]")
    parser.add_argument("external_address", action="store", type=str, help="listener external address")
    parser.add_argument("port", action="store", type=int, help="listener port")
    args = parser.parse_args()
