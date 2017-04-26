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
