import pymysql
from core.config import *


class WebServer(object):

    def __init__(self, protocol, external_address, port, profile):
        self.protocol = protocol
        self.external_address = external_address
        self.port = port
        self.profile = profile

        self.app = Flask(__name__)
        self.app.debug = True

        # tries to establish a connection to the database
        try:
            self.connection = pymysql.connect(
                host="localhost",
                port=3306,
                user=username,
                passwd=password,
                db=database,
                autocommit=True)

        except Exception:
            raise
