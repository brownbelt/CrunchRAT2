#!/bin/bash

# Bash bold coloring
DEFAULT="\e[39m\e[1m"
RED="\e[31m\e[1m"
GREEN="\e[32m\e[1m"

# If script did not run with root or sudo privileges
# Exits the script
if [ "$(id -u)" != "0" ];
then
    echo -e "${RED}[-] You must run this script with root or sudo privileges.${DEFAULT}\n"
    exit 1
fi

# Gets operating system
OS_NAME=`cat /etc/os-release | grep -i "PRETTY_NAME" | awk -F= '{print $2}' | sed -e 's/"//g'`

# If Ubuntu 16.04
if [[ $OS_NAME == *"Ubuntu 16.04"* ]]
then
    echo -e "${GREEN}[+] Ubuntu 16.04 detected ${DEFAULT}\n"

    # Updates repositories
    echo -e "${GREEN}[+] Updating ${DEFAULT}\n"
    sudo apt-get update

    # Installs all Ubuntu 16.04 dependencies
    echo -e "\n${GREEN}[+] Installing dependencies ${DEFAULT}\n"
    sudo apt-get install -y apache2
    sudo apt-get install -y mysql-server
    sudo apt-get install -y php libapache2-mod-php php-mcrypt php-mysql

# Else if Ubuntu 14.04
elif [[ $OS_NAME == *"Ubuntu 14.04"* ]]
then
    echo -e "${GREEN}[+] Ubuntu 14.04 detected ${DEFAULT}\n"
    
    # Updates repositories
    echo -e "${GREEN}[+] Updating ${DEFAULT}\n"
    sudo apt-get update

    # TO DO: Install all Ubuntu 14.04 dependencies here

# Else invalid operating system
# Exits program
else
    echo -e "${RED}[-] Invalid operating system ${DEFAULT}\n"
    exit 1
fi

# TO DO: MySQL database and table setup here

# TO DO: Create /var/log/CrunchRAT directory and chown it to "www-data"
# Make it a green status bar letting the user know it's creating this directory as well
sudo mkdir /var/log/CrunchRAT
sudo chown www-data:www-data /var/log/CrunchRAT
