#!/bin/bash

# Bash bold coloring
DEFAULT="\e[39m\e[1m"
RED="\e[31m\e[1m"
GREEN="\e[32m\e[1m"

# Gets operating system
OS_NAME=`cat /etc/os-release | grep -i "PRETTY_NAME" | awk -F= '{print $2}' | sed -e 's/"//g'`

# If Ubuntu 16.04
if [[ $OS_NAME == *"Ubuntu 16.04"* ]]
then
    echo -e "${GREEN}[+] Ubuntu 16.04 detected ${DEFAULT}\n"
    VERSION="16.04"
# Else if Ubuntu 14.04
elif [[ $OS_NAME == *"Ubuntu 14.04"* ]]
then
    echo -e "${GREEN}[+] Ubuntu 14.04 detected ${DEFAULT}\n"
    VERSION="14.04"
# Else invalid operating system
# Exits program
else
    echo -e "${RED}[-] Invalid operating system ${DEFAULT}\n"
    exit 1
fi
