import ipaddress
import json
import socket
import sys
from colorama import Fore, Style


class ArgChecks(object):
    def __init__(self, protocol, external_address, port):
        self.protocol = protocol
        self.external_address = external_address
        self.port = port

    def protocol_check(self):
        if self.protocol != "http" and self.protocol != "https":
            print(Style.BRIGHT + Fore.RED + '[!] Invalid protocol supplied. Please enter "http" or "https".' + Style.RESET_ALL)
            sys.exit()

    def external_address_check(self):
        try:
            ipaddress.ip_address(self.external_address)

        except:
            print(Style.BRIGHT + Fore.RED + "[!] Invalid external address supplied." + Style.RESET_ALL)
            sys.exit()

    def port_check(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect(("localhost", self.port))
            print(Style.BRIGHT + Fore.RED + "[!] Port already in use. Please choose another port." + Style.RESET_ALL)
            sys.exit()

        except:
            pass
