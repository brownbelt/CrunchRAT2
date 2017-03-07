# CrunchRAT 2.0 Python 2.x Implant

import getpass
import os
import platform
import socket
import sys


def get_system_info():
    '''
       Purpose: Collects system information
        Returns: hostname (str), current_user (str), process_id (int), operating_system (str)
    '''
    hostname = socket.gethostname()
    current_user = getpass.getuser()
    process_id = os.getpid()

    # If operating system is Mac OS X
    if "Darwin" in platform.system():
        operating_system = "Mac OS X " + platform.mac_ver()[0]
    # Else operating system is Linux
    else:
        operating_system = platform.linux_distribution()[0] + " " + platform.linux_distribution()[1]

    return (hostname, current_user, process_id, operating_system)


if __name__ == "__main__":
    hostname, current_user, process_id, operating_system = get_system_info()
