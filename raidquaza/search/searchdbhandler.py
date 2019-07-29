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
from typing import List


class SearchDBHandler(DbHandler):

    def __init__(self, host, database, port, user, password, dialect, driver):
        super(SearchDBHandler, self).__init__(host, database, port, user, password, dialect, driver)

    def fetch_results(self, table, type):
        if type == RECORD_TYPE.PORTAL:
            query_result = self.session.execute(f"SELECT name, lat, lon FROM {table}")
        else:
            query_result = self.session.execute(f"SELECT name, latitude, longitude FROM {table}")
        results = [Record(*r, type) for r in query_result.fetchall()]
        return results

    @transaction_wrapper
    def get_pois(self, table: str, type: RECORD_TYPE) -> List[Record]:
        # Fetch poi from DB table
        pois = self.fetch_results(table=table, type=type)
        LOGGER.info("Pulled %d pois of type %s from table %s" % (len(pois), type, table))
        return pois


if __name__ == '__main__':
    db = SearchDBHandler(host="localhost", user="monocleuser", password="test123", port="3309", database="monocledb",
                         dialect="mysql", driver="mysqlconnector")
    forts = db.get_pois(table=config.SEARCH_GYM_TABLE + " JOIN gymdetails ON gym.gym_id = gymdetails.gym_id",
                        type=RECORD_TYPE.GYM)
    stops = db.get_pois(table=config.SEARCH_POKESTOP_TABLE, type=RECORD_TYPE.POKESTOP)
    portals = db.get_pois(table=config.SEARCH_PORTALS_DB_TABLE, type=RECORD_TYPE.PORTAL)
    print(len(forts), forts)
    print(len(stops), stops)
    print(len(portals), portals)
