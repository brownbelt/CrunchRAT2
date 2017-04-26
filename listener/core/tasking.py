import pymysql
from core.config import *


class Tasking(object):

    def __init__(self):
        # tries to open a database connection
        try:
            self.connection = pymysql.connect(host="localhost",
                                              port=3306,
                                              user=username,
                                              passwd=password,
                                              db=database,
                                              autocommit=True)

        except Exception:
            raise

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

        # tries to check tasking
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

        # finally closes database connection
        finally:
            self.connection.close()
