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


class FuzzySearcher(object):

    def __init__(self, input_file, q=3, k=5):
        self.q = q
        self.k = k
        # init search engine
        self.fuzzy = QgramIndex(3)
        # build index
        self.fuzzy.build_from_file(input_file)

    def search(self, query):
        print("Query: " + query)
        query = re.sub("[ \W+\n]", "", query).lower()
        query = re.sub("%", " ", query).lower()
        k = 5
        delta = int(math.floor(len(query) / 4))
        #delta = 3
        result = self.fuzzy.find_matches(query, delta, k, True)
        return result



