from typing import Union
import json

from poll.poll import Poll
from poll.dbhandler import DbHandler
from config.Configuration import Configuration


class PollManager(object):

    def __init__(self, config: Configuration):
        self.polls = dict()
        self.received_message_to_poll = dict()
        self.sent_message_to_poll = dict()
        self.db = DbHandler(database=config.poll_db_database, user=config.poll_db_user,
                            password=config.poll_db_password, host=config.poll_db_host,
                            dialect=config.poll_db_dialect, driver=config.poll_db_driver,
                            port=config.poll_db_port)

    def add_poll(self, poll: Poll, sent_message, received_message):
        self.polls[poll.poll_id] = poll
        self.sent_message_to_poll[sent_message] = poll.poll_id
        self.received_message_to_poll[received_message] = poll.poll_id

    def is_sent_message(self, msg_id: int) -> bool:
        return msg_id in self.sent_message_to_poll

    def get_poll_by_id(self, poll_id: str) -> Union[Poll, None]:
        if poll_id in self.polls:
            return self.polls[poll_id]
        else:
            return None

    def get_poll_by_msg_id(self, msg_id: int) -> Union[Poll, None]:
        if msg_id in self.sent_message_to_poll:
            poll_id = self.sent_message_to_poll[msg_id]
            if poll_id in self.polls:
                return self.polls[poll_id]
            else:
                return None

    def serialize_json(self, poll: Poll):
        dt = {}
        dt.update(vars(poll))
        return dt

    def deserialize_json(self, data):
        data = json.load(data)
        instance = object.__new__(Poll)
        for key, value in data.items():
            setattr(instance, key, value)

        return instance
