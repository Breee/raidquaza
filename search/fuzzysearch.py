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
from globals.globals import LOGGER
from search.dbmanager import SearchDatabaseHandler
from config.Configuration import DataSource, Configuration


class FuzzySearcher(object):

    def __init__(self, config: Configuration, q=3, k=5):
        self.q = q
        self.k = k
        # init search engine
        self.index(config)

    def index(self, config):
        self.point_of_interest_index = PointOfInterestQgramIndex(3, config)
        input = None
        if config.data_source == DataSource.DATABASE:
            LOGGER.info("Using database")
            self.db_handler = SearchDatabaseHandler(host=config.search_db_host, db=config.search_db_name,
                                                    port=config.search_db_port,
                                                    user=config.search_db_user, password=config.search_db_password,
                                                    pokestop_table_name=config.pokestop_table_name,
                                                    gym_table_name=config.gym_table_name)
            forts, stops = self.db_handler.get_gyms_stops()
            input = [*forts, *stops]
            self.db_handler.disconnect()

        if isinstance(input, list):
            LOGGER.info("Using forts/stops from database")
            self.point_of_interest_index.build_from_lists(input)
        else:
            LOGGER.info("Using forts/stops from file")
            input = config.point_of_interests
            self.point_of_interest_index.build_from_file(input)

    def search(self, query, num_results=5, channel_id=None):
        LOGGER.info("Received query %s " % query)
        query = re.sub("[ \W+\n]", "", query).lower()
        query = re.sub("%", " ", query).lower()
        delta = int(math.floor(len(query) / 4))
        result = self.point_of_interest_index.find_matches(query, delta, k=num_results, use_qindex=True,
                                                           channel_id=channel_id)
        return result
