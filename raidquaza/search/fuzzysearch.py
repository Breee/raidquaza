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
import math
import re
from search.qgram_index import PointOfInterestQgramIndex
from utility.globals import LOGGER
from search.searchdbhandler import SearchDBHandler
from utility.enums import DataSource
from search.enums import RECORD_TYPE


class FuzzySearcher(object):

    def __init__(self, config, q=3, k=5):
        self.q = q
        self.k = k
        # init search engine
        self.db_handler = None
        self.point_of_interest_index: PointOfInterestQgramIndex = None
        self.config = config
        self.index()

    def index(self):
        self.point_of_interest_index = PointOfInterestQgramIndex(3, self.config.SEARCH_USE_GEOFENCES,
                                                                 self.config.SEARCH_CHANNELS_TO_GEOFENCES)
        index_input = []
        if self.config.SEARCH_DATASOURCE == DataSource.DATABASE:
            LOGGER.info("Using database")
            self.db_handler = SearchDBHandler(database=self.config.SEARCH_DB_NAME,
                                              user=self.config.SEARCH_DB_USER,
                                              password=self.config.SEARCH_DB_PASSWORD,
                                              host=self.config.SEARCH_DB_HOST,
                                              dialect=self.config.SEARCH_DB_DIALECT,
                                              driver=self.config.SEARCH_DB_DRIVER,
                                              port=self.config.SEARCH_DB_PORT)
            forts = self.db_handler.get_pois(table=self.config.SEARCH_GYM_TABLE, type=RECORD_TYPE.GYM)
            stops = self.db_handler.get_pois(table=self.config.SEARCH_POKESTOP_TABLE, type=RECORD_TYPE.POKESTOP)
            index_input += [*forts] + [*stops]
        if self.config.SEARCH_USE_PORTALS:
            if self.config.SEARCH_PORTALS_DATASOURCE == DataSource.DATABASE:
                self.db_handler = SearchDBHandler(database=self.config.SEARCH_PORTALS_DB_NAME,
                                                  user=self.config.SEARCH_PORTALS_DB_USER,
                                                  password=self.config.SEARCH_PORTALS_DB_PASSWORD,
                                                  host=self.config.SEARCH_PORTALS_DB_HOST,
                                                  dialect=self.config.SEARCH_PORTALS_DB_DIALECT,
                                                  driver=self.config.SEARCH_PORTALS_DB_DRIVER,
                                                  port=self.config.SEARCH_PORTALS_DB_PORT)
                portals = self.db_handler.get_pois(table=self.config.SEARCH_PORTALS_DB_TABLE, type=RECORD_TYPE.PORTAL)
                index_input += [*portals]

        if isinstance(index_input, list) and index_input:
            LOGGER.info("Using forts/stops from database")
            self.point_of_interest_index.build_from_lists(index_input)
        else:
            LOGGER.info("Using forts/stops from file")
            index_input = self.config.SEARCH_CSV_FILE
            self.point_of_interest_index.build_from_file(index_input)

    def search(self, query, num_results=5, channel_id=None):
        LOGGER.info("Received query %s " % query)
        query = re.sub("[ \W+\n]", "", query).lower()
        query = re.sub("%", " ", query).lower()
        delta = int(math.floor(len(query) / 4))
        result = self.point_of_interest_index.find_matches(query, k=num_results, use_qindex=True,
                                                           channel_id=channel_id)
        return result
