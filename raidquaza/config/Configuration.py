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

from configparser import ConfigParser
import json
import os
import enum


class DataSource(enum.Enum):
    CSV = 1,
    DATABASE = 2


class Configuration(object):

    def __init__(self, config_file):
        self.token = ""
        self.prefix = "!"
        self.playing = ""
        self.use_search = False
        self.data_source = DataSource.CSV
        self.use_geofences = False
        self.use_polls = False
        self.csv_file = ""
        self.search_db_host = ""
        self.search_db_name = ""
        self.search_db_user = ""
        self.search_db_password = ""
        self.search_db_port = 3306
        self.pokestop_table_name = "pokestops"
        self.gym_table_name = "forts"
        self.channel_to_geofences = dict()
        self.use_polls = None
        self.poll_db_host = None
        self.poll_db_user = None
        self.poll_db_password = None
        self.poll_db_port = None
        self.poll_db_database = None
        self.poll_db_dialect = None
        self.poll_db_driver = None
        self.parser = ConfigParser()
        self.read_config_file(config_file)

    def read_config_file(self, filename='config.ini.example'):
        """ Read configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        >>> c = Configuration(config_file='config.ini.example')
        >>> c.token
        '<bot_token>'

        """
        self.parser.read(filename)

        # BOT SECTION
        if self.parser.has_section('bot'):
            bot_section = self.parser['bot']
            if 'token' not in bot_section:
                raise Exception("No Bot Token specified, this is required")
            else:
                self.token = bot_section['token']

            if 'playing' in bot_section:
                self.playing = bot_section['playing']

            if 'prefix' in bot_section:
                self.prefix = bot_section['prefix']
        else:
            raise Exception(f'bot section not found in config {filename}, this is required')

        # SEARCH SECTION
        if self.parser.has_section('search'):
            self.use_search = True
            search_section = self.parser['search']
            if 'data_source' in search_section:
                data_source = search_section['data_source']
                if data_source == 'database':
                    self.data_source = DataSource.DATABASE
                elif data_source == 'csv':
                    self.data_source = DataSource.CSV
                else:
                    raise Exception(f'datasource {data_source} unknown, choose: database / csv')

            if self.data_source == DataSource.DATABASE:
                self.search_db_host = search_section['host']
                self.search_db_name = search_section['database']
                self.search_db_user = search_section['user']
                self.search_db_password = search_section['password']
                self.search_db_port = search_section['port']
                self.pokestop_table_name = search_section['pokestop_table_name']
                self.gym_table_name = search_section['gym_table_name']
            elif self.data_source == DataSource.CSV:
                self.csv_file = search_section['csv_file']
            # GEOFENCES
            if 'use_geofences' in search_section:
                self.use_geofences = search_section['use_geofences']
            if self.use_geofences:
                geofences = [os.path.abspath(x) for x in json.loads(search_section['geofences'])]
                channels = json.loads(search_section['channels'])
                if not geofences or not channels or len(channels) != len(geofences):
                    raise Exception("The Number of channels must match number of geofences.\n"
                                    "Both are lists, defining a one-to-one mapping channels[i] -> geofences[i].\n"
                                    "Example:\n\n"
                                    "geofences = ['geofencefile1.txt']\nchannels = ['discord_channel_id_1']\n"
                                    "--> To define that in channel << discord_channel_id_1 >> we only search for "
                                    "coordinates that lay in the geofence defined by << geofencefile1.txt >>")
                self.channel_to_geofences = dict(zip(channels, geofences))

        # POLLS
        if self.parser.has_section('polls'):
            poll_section = self.parser['polls']
            self.use_polls = True
            self.poll_db_host = poll_section['host']
            self.poll_db_user = poll_section['user']
            self.poll_db_password = poll_section['password']
            self.poll_db_port = poll_section['port']
            self.poll_db_database = poll_section['database']
            self.poll_db_dialect = poll_section['dialect']
            self.poll_db_driver = poll_section['driver']
