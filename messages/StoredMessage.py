import logging
import time
logger = logging.getLogger('discord')


class StoredMessage(object):
    def __init__(self, id, commandmessage, postedmessage):
        self.id = id
        self.creation_time = time.time()
        self.commandmessage = commandmessage
        self.postedmessage = postedmessage

