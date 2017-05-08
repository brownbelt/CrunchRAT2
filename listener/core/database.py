from config import *
import pymysql


class Database(object):

    @staticmethod
    def open_connection():
        """
        DESCRIPTION:
            This function opens a database connection
        """
        # tries to open database connection
        try:
            connection = pymysql.connect(host="localhost",
                                         port=port,
                                         user=username,
                                         passwd=password,
                                         db=database,
                                         autocommit=True)

            return connection

        # exception raised opening database connection
        except Exception:
            raise

    @staticmethod
    def close_connection(connection):
        """
        DESCRIPTION:
            This function closes a database connection
        """
        if connection.open is True:
            connection.close
