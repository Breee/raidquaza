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
import pickle
import os
from storage.Storage import Storage
LOGGER = logging.getLogger('discord')


class StorageManager(object):
    def __init__(self):
        self.storage = None
        self.dump_file_name = "storage.pickle"

    def update_storage(self, message_manager,  client_messages):
        self.storage = Storage(message_manager=message_manager, client_messages=client_messages)
        self.dump_storage()

    def dump_storage(self):
        LOGGER.info("Dumping Storage to %s" % self.dump_file_name)
        with open(self.dump_file_name, 'wb') as dump:
            pickle.dump(self.storage, dump, protocol=pickle.HIGHEST_PROTOCOL)
            LOGGER.info("Dumping Storage was successful")

    def load_storage(self):
        LOGGER.info("Loading Storage from %s" % self.dump_file_name)
        if os.path.isfile(self.dump_file_name):
            if os.stat(self.dump_file_name).st_size != 0:
                with open(self.dump_file_name, 'rb') as dump:
                    self.storage = pickle.load(dump)
                    LOGGER.info("Loading Storage was successful.")
                    return self.storage


