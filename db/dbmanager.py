"""
MIT License

Copyright (c) 2018 Breee@github

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from mysql.connector import MySQLConnection, Error
import logging
from globals.globals import LOGGER

class DbHandler(object):

    def __init__(self, host, db, port, user, password,pokestop_table_name, gym_table_name):
        self.host = host
        self.db = db
        self.port = port
        self.user = user
        self.password = password
        self.pokestop_table_name = pokestop_table_name
        self.gym_table_name = gym_table_name
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
        self.cursor.execute(f"SELECT name, lat, lon FROM {self.gym_table_name}")
        for row in self.cursor:
            if row[0]:
                forts.append(row + ('Arena',))

        self.cursor.execute(f"SELECT name, lat, lon FROM {self.pokestop_table_name}")
        for row in self.cursor:
            if row[0]:
                stops.append(row + ('Pokestop',))
        LOGGER.info("Pulled %d forts and %d stops" % (len(forts), len(stops)))
        return forts, stops


if __name__ == '__main__':
    db = DbHandler(host = 'localhost', db = 'monocle', user = 'monocleuser', password = 'test123', port = 3306)
    forts, stops = db.get_forts_stops()
    print(len(forts), forts)
    print(len(stops), stops)
    db.disconnect()

