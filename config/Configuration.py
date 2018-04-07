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
