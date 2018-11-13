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

import logging
import math
import re
from search.qgram_index import QgramIndex
LOGGER = logging.getLogger('discord')
from db.dbmanager import DbHandler


class FuzzySearcher(object):

    def __init__(self,config, q=3, k=5):
        self.q = q
        self.k = k
        # init search engine
        self.fuzzy = QgramIndex(3)
        # build index
        input = None
        if config.use_database:
            LOGGER.info("Using database")
            self.db_handler = DbHandler(host=config.db_host, db=config.db_name, port=config.db_port,
                                        user=config.db_user, password=config.db_password)
            forts,stops = self.db_handler.get_forts_stops()
            input = [*forts, *stops]
            self.db_handler.disconnect()

        if isinstance(input, list):
            LOGGER.info("Using forts/stops from database")
            self.fuzzy.build_from_lists(input)
        else:
            LOGGER.info("Using forts/stops from file")
            input = config.point_of_interests
            self.fuzzy.build_from_file(input)

    def search(self, query, num_results=5):
        LOGGER.info("Received query %s " % query)
        query = re.sub("[ \W+\n]", "", query).lower()
        query = re.sub("%", " ", query).lower()
        delta = int(math.floor(len(query) / 4))
        result = self.fuzzy.find_matches(query, delta, k=num_results, use_qindex=True)
        return result



