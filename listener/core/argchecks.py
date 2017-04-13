import ipaddress
import json
import socket
import sys
from colorama import Fore, Style


class ArgChecks(object):
    def __init__(self):
        self.protocol = None
        self.external_address = None
        self.port = None
        self.profile = None

    def protocol_check(self, protocol):
        if protocol != "http" and protocol != "https":
            print(Style.BRIGHT + Fore.RED + '[!] Invalid protocol supplied. Please enter "http" or "https".' + Style.RESET_ALL)
            sys.exit(0)

        else:
            self.protocol = protocol

    def external_address_check(self, external_address):
        try:
            ipaddress.ip_address(external_address)
            self.external_address = external_address

        except:
            print(Style.BRIGHT + Fore.RED + "[!] Invalid external address supplied." + Style.RESET_ALL)
            sys.exit(0)

    def port_check(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect(("localhost", port))
            print(Style.BRIGHT + Fore.RED + "[!] Port already in use. Please choose another port." + Style.RESET_ALL)
            sys.exit(0)

        except:
            self.port = port

    def profile_check(self, profile):
        try:
            with open(profile) as f:
                self.profile = json.loads(f.read())

        except:
            print(Style.BRIGHT + Fore.RED + "[!] Error parsing the provided JSON profile." + Style.RESET_ALL)
            sys.exit(0)
