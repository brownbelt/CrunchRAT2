#!/bin/bash

# coloring
RED=$'\e[1;31m'
GREEN=$'\e[1;32m'
END=$'\e[0m'

# if script was not run as sudo/root
if [[ $(id -u) -ne 0 ]]
  then echo "${RED}[!] Please re-run with sudo/root privileges.${END}"
  exit
fi

# TO DO: check if sqlite3 is installed

# creates database and associated tables
sqlite3 ../rat.db < database_setup.sql
