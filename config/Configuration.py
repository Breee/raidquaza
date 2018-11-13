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
from configparser import ConfigParser

logger = logging.getLogger('discord')

class Configuration(object):

    def __init__(self, config_file):
        self.token = ""
        self.playing = ""
        self.point_of_interests = "../data/gyms_stops.csv"
        self.use_database = False
        self.db_host = ""
        self.db_name = ""
        self.db_user = ""
        self.db_password = ""
        self.db_port = 3306
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
            logger.info('{0} not found in the {1} file, assuming no csv used'.format('bot', filename))

        if parser.has_section('mysql'):
            items = parser.items('mysql')
            for item in items:
                conf[item[0]] = item[1]
        else:
            logger.info('{0} not found in the {1} file, assuming no database used'.format('bot', filename))

        if not parser.has_section('csv') and not parser.has_section('mysql'):
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
                logger.info("No password set, assuming none.")
            if 'port' in conf.keys():
                self.db_port = conf['port']
            else:
                logger.info("No port set, assuming %d." % self.db_port)

















