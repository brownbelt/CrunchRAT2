import argparse
from core.webserver import WebServer

parser = argparse.ArgumentParser(prog="listener.py", description="CrunchRAT2 Listener - Written by Hunter Hardman @t3ntman")
parser.add_argument("protocol", action="store", type=str, help="listener protocol [http][https]")
parser.add_argument("external_address", action="store", type=str, help="listener external address")
parser.add_argument("port", action="store", type=int, help="listener port")
parser.add_argument("profile", action="store", type=str, help="listener profile")

# parses command-line arguments
args = parser.parse_args()

WebServer().start_flask(args.protocol, args.port, args.profile)
