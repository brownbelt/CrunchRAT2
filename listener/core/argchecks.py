import ipaddress
import json
import socket
import sys
from colorama import Fore, Style


class ArgChecks(object):
    def __init__(self, protocol, external_address, port, profile):
        self.protocol = protocol
        self.external_address = external_address
        self.port = port
        self.profile = profile

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

        except OverflowError:
            print(Style.BRIGHT + Fore.RED + "[!] Invalid port supplied. Please choose a port between 1-65535." + Style.RESET_ALL)
            sys.exit()

        except socket.error:
            pass

    def profile_check(self):
        # TO DO: add in profile check here
