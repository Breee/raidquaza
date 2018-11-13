from mysql.connector import MySQLConnection, Error
import logging
LOGGER = logging.getLogger('discord')

class DbHandler(object):

    def __init__(self, host, db, port, user, password):
        self.host = host
        self.db = db
        self.port = port
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None
        try:
            config = {'user': self.user,
                      'password': self.password,
                      'database': self.db,
                      'host': self.host,
                      'port': self.port}
            LOGGER.info('Connecting to MySQL database...')
            self.conn = MySQLConnection(**config)
            self.cursor = self.conn.cursor()

            if self.conn.is_connected():
                LOGGER.info('connection established.')
            else:
                raise Exception('connection to database failed.')

        except Error as error:
            raise Exception(error)

    def disconnect(self):
        self.conn.close()
        LOGGER.info("disconnected from DB")

    def get_forts_stops(self):
        LOGGER.info("Pulling forts and stops from DB")
        forts = []
        stops = []
        self.cursor.execute("SELECT name, lat, lon FROM forts")
        for row in self.cursor:
            forts.append(row + ('Arena',))

        self.cursor.execute("SELECT name, lat, lon FROM pokestops")
        for row in self.cursor:
            stops.append(row + ('Pokestop',))
        LOGGER.info("Done.")
        return forts, stops


if __name__ == '__main__':
    db = DbHandler(host = 'localhost', db = 'monocle', user = 'monocleuser', password = 'test123', port = 3306)
    forts, stops = db.get_forts_stops()
    print(len(forts), forts)
    print(len(stops), stops)
    db.disconnect()

