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
from globals.globals import LOGGER
import json
import os

class Configuration(object):

    def __init__(self, config_file):
        self.token = ""
        self.playing = ""
        self.point_of_interests = ""
        self.use_database = False
        self.db_host = ""
        self.db_name = ""
        self.db_user = ""
        self.db_password = ""
        self.db_port = 3306
        self.pokestop_table_name = "pokestops"
        self.gym_table_name = "forts"
        self.use_geofences = False
        self.channel_to_geofences = dict()
        self.read_config_file(config_file)

    def read_config_file(self, filename='config.ini.example'):
        """ Read configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        >>> c = Configuration(config_file='config.ini.example')
        >>> c.token
        '<bot_token>'
        >>> c.playing
        'u mom lel'
        >>> c.point_of_interests
        '../data/gyms_stops.csv'
        >>> c.use_database
        True
        >>> c.db_host
        'localhost'
        >>> c.db_name
        'db_name'
        >>> c.db_user
        'user_name'
        >>> c.db_password
        'password'
        >>> c.channel_to_geofences
        {12321425124: '/home/bree/repos/pokemon-discord-report-bot/config/config/geofence1.txt'}
        >>> c.pokestop_table_name
        'pokestops'
        >>> c.gym_table_name
        'forts'

        """
        # create parser and read ini configuration file
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to mysql
        conf = {}
        if parser.has_section('bot'):
            items = parser.items('bot')
            for item in items:
                conf[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format('bot', filename))

        if parser.has_section('csv'):
            items = parser.items('csv')
            for item in items:
                conf[item[0]] = item[1]
        else:
            LOGGER.warning('{0} not found in the {1} file, assuming no csv provided'.format('csv', filename))

        if parser.has_section('database'):
            items = parser.items('database')
            for item in items:
                conf[item[0]] = item[1]
        else:
            LOGGER.warning('{0} not found in the {1} file, assuming no database used'.format('bot', filename))

        if parser.has_section('geofences'):
            items = parser.items('geofences')
            for item in items:
                conf[item[0]] = item[1]
        else:
            LOGGER.warning('{0} not found in the {1} file, assuming no database used'.format('bot', filename))

        if not parser.has_section('csv') and not parser.has_section('database'):
            raise Exception('No csv file or database specified, please do at least one.')

        if 'token' in conf.keys():
            self.token = conf['token']
        else:
            raise Exception("No Bot Token specified, this is required")

        if 'playing' in conf.keys():
            self.playing = conf['playing']

        if 'point_of_interests' in conf.keys():
            self.point_of_interests = conf['point_of_interests']

        if 'use_database' in conf.keys():
            if conf['use_database'] == 'True':
                self.use_database = True

        if self.use_database:
            if 'host' in conf.keys():
                self.db_host = conf['host']
            else:
                raise Exception("use_database = true, host is required")
            if 'database' in conf.keys():
                self.db_name = conf['database']
            else:
                raise Exception("use_database = true, database is required")
            if 'user' in conf.keys():
                self.db_user = conf['user']
            else:
                raise Exception("use_database = true, database user is required")
            if 'password' in conf.keys():
                self.db_password = conf['password']
            else:
                LOGGER.warning("No password set, assuming none.")
            if 'port' in conf.keys():
                self.db_port = conf['port']
            else:
                LOGGER.warning("No port set, assuming %d." % self.db_port)

            if 'pokestop_table_name' in conf.keys():
                self.pokestop_table_name = conf['pokestop_table_name']
            else:
                LOGGER.warning("No pokestop_table_name set, assuming %d." % self.pokestop_table_name)

            if 'gym_table_name' in conf.keys():
                self.gym_table_name = conf['gym_table_name']
            else:
                LOGGER.warning("No pokestop_table_name set, assuming %d." % self.pokestop_table_name)

        if 'use_geofences' in conf.keys():
            if conf['use_geofences'] == 'True':
                self.use_geofences = True

        if self.use_geofences:
            geofences = None
            channels = None
            if 'geofences' in conf.keys():
                geofences = json.loads(conf['geofences'])
                geofences = [os.path.abspath(x) for x in geofences]
            if 'channels' in conf.keys():
                channels = json.loads(conf['channels'])

            if not geofences or not channels or len(channels) != len(geofences):
                raise Exception("You specified to use geofences.\n"
                                "The Number of channels must match number of geofences.\n"
                                "Both are lists, defining a one-to-one mapping channels[i] -> geofences[i].\n"
                                "Example:\n\n"
                                "geofences = ['geofencefile1.txt']\nchannels = ['discord_channel_id_1']\n"
                                "--> To define that in channel << discord_channel_id_1 >> we only search for coordinates that lay in the geofence defined by << geofencefile1.txt >>")
            self.channel_to_geofences = dict(zip(channels, geofences))




















