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
import time
logger = logging.getLogger('discord')

class Configuration(object):

    def __init__(self, config_file):
        self.token = ""
        self.playing = ""
        self.server_id = ""
        self.quest_channel_id = ""
        self.rare_channel_id = ""
        self.raid_channel_id = ""
        self.nest_channel_id = ""
        self.gyms_csv = ""
        self.bitly_access_token = ""
        self.read_config_file(config_file)

    def read_config_file(self, config_file):
        """
        >>> Conf = Configuration("test.conf")
        >>> Conf.token
        'TESTTOKEN'
        >>> Conf.playing
        'TESTPLAYING'
        :param config_file:
        :return:
        """
        with open(config_file, 'r') as config:
            for line in config:
                if line.startswith("token="):
                    self.token = line[line.find("=") + 1:].rstrip("\n")
                if line.startswith("playing="):
                    self.playing = line[line.find("=") + 1:].rstrip("\n")
                if line.startswith("raid-channel-id="):
                    self.raid_channel_id = line[line.find("=") + 1:].rstrip("\n")
                if line.startswith("rare-channel-id="):
                    self.rare_channel_id = line[line.find("=") + 1:].rstrip("\n")
                if line.startswith("quest-channel-id="):
                    self.quest_channel_id = line[line.find("=") + 1:].rstrip("\n")
                if line.startswith("nest-channel-id="):
                    self.nest_channel_id = line[line.find("=") + 1:].rstrip("\n")
                if line.startswith("gyms-csv="):
                    self.gyms_csv = line[line.find("=") + 1:].rstrip("\n")
                if line.startswith("bitly-access-token="):
                    self.bitly_access_token = line[line.find("=") + 1:].rstrip("\n")



