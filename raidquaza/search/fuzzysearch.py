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
import config as config


class FuzzySearcher(object):

    def __init__(self, q=3, k=5):
        self.q = q
        self.k = k
        # init search engine
        self.db_handler = None
        self.point_of_interest_index: PointOfInterestQgramIndex = None
        self.index()

    def index(self):
        self.point_of_interest_index = PointOfInterestQgramIndex(3, config.SEARCH_USE_GEOFENCES,
                                                                 config.SEARCH_CHANNELS_TO_GEOFENCES)
        index_input = None
        if config.SEARCH_DATASOURCE == DataSource.DATABASE:
            LOGGER.info("Using database")
            self.db_handler = SearchDBHandler(database=config.SEARCH_DB_NAME, user=config.SEARCH_DB_USER,
                                              password=config.SEARCH_DB_PASSWORD, host=config.SEARCH_DB_HOST,
                                              dialect=config.SEARCH_DB_DIALECT, driver=config.SEARCH_DB_DRIVER,
                                              port=config.SEARCH_DB_PORT)
            forts, stops = self.db_handler.get_gyms_stops()
            index_input = [*forts, *stops]

        if isinstance(index_input, list):
            LOGGER.info("Using forts/stops from database")
            self.point_of_interest_index.build_from_lists(index_input)
        else:
            LOGGER.info("Using forts/stops from file")
            index_input = config.SEARCH_CSV_FILE
            self.point_of_interest_index.build_from_file(index_input)

    def search(self, query, num_results=5, channel_id=None):
        LOGGER.info("Received query %s " % query)
        query = re.sub("[ \W+\n]", "", query).lower()
        query = re.sub("%", " ", query).lower()
        delta = int(math.floor(len(query) / 4))
        result = self.point_of_interest_index.find_matches(query, delta, k=num_results, use_qindex=True,
                                                           channel_id=channel_id)
        return result
