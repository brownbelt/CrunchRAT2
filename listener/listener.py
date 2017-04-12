import argparse


if __name__ == "__main__":
    # TO DO: add in checks for python 2.x

    # TO DO: add in sudo checks

    # parses arguments
    parser = argparse.ArgumentParser(prog="listener.py", description="CrunchRAT2 Listener - Written by Hunter Hardman @t3ntman")
    parser.add_argument("protocol", nargs="?", type=str, help="listener protocol [http][https]")
    parser.add_argument("address", nargs="?", type=str, help="listener address")
    parser.add_argument("port", nargs="?", type=int, help="listener port")
    parser.add_argument("profile", nargs="?", type=argparse.FileType("r"), help="json profile")
    args = parser.parse_args()

    # saves provided arguments
    protocol = args.protocol
    address = args.address
    port = args.port
    profile = args.profile
