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

from utility.globals import LOGGER
from search.enums import RECORD_TYPE
from database.dbhandler import DbHandler, transaction_wrapper
import config as config
from utility.custom_types import Record


class SearchDBHandler(DbHandler):

    def __init__(self, host, database, port, user, password, dialect, driver):
        super(SearchDBHandler, self).__init__(host, database, port, user, password, dialect, driver)

    @transaction_wrapper
    def get_gyms_stops(self):
        LOGGER.info("Pulling forts and stops from DB")
        gyms = []
        stops = []

        #  Fetch gyms from DB
        gym_result = self.session.execute(f"SELECT name, lat, lon FROM {config.SEARCH_GYM_TABLE}")
        gym_records = [Record(*r, RECORD_TYPE.GYM) for r in gym_result.fetchall()]
        for row in gym_records:
            gyms.append(row)

        # Fetch stops from DB
        pokestop_result = self.session.execute(f"SELECT name, lat, lon FROM {config.SEARCH_POKESTOP_TABLE}")
        pokestop_records = [Record(*r, RECORD_TYPE.POKESTOP) for r in pokestop_result.fetchall()]
        for row in pokestop_records:
            stops.append(row)
        LOGGER.info("Pulled %d forts and %d stops" % (len(gyms), len(stops)))
        return gyms, stops


if __name__ == '__main__':
    db = SearchDBHandler(host="localhost", user="monocleuser", password="test123", port="3309", database="monocledb",
                         dialect="mysql", driver="mysqlconnector")
    forts, stops = db.get_gyms_stops()
    print(len(forts), forts)
    print(len(stops), stops)
