from typing import Union
import json

from poll.polls import Poll
from poll.polldbhandler import PollDBHandler
import config as config


class PollManager(object):

    def __init__(self):
        self.polls = dict()
        self.received_message_to_poll = dict()
        self.sent_message_to_poll = dict()
        self.db = PollDBHandler(database=config.POLL_DB_NAME, user=config.POLL_DB_USER,
                                password=config.POLL_DB_PASSWORD, host=config.POLL_DB_HOST,
                                dialect=config.POLL_DB_DIALECT, driver=config.POLL_DB_DRIVER,
                                port=config.POLL_DB_PORT)
        self.pull_polls_from_db()

    def pull_polls_from_db(self):
        polls = self.db.get_polls()
        if polls:
            for poll in polls:
                poll_obj = Poll(poll_id=poll.poll_id,
                                poll_title=poll.poll_title,
                                options=poll.options,
                                is_immortal=poll.is_immortal,
                                updated_since_start=False)
                poll_obj.creation_time = poll.creation_time
                poll_obj.last_update = poll.last_update
                poll_obj.received_message = poll.received_message
                poll_obj.sent_message = poll.sent_message
                poll_obj.reaction_to_option = poll.reaction_to_option
                poll_obj.option_to_reaction = poll.option_to_reaction
                poll_obj.reactions = poll.reactions
                poll_obj.participants = poll.participants
                poll_obj.option_to_participants = poll.option_to_participants
                poll_obj.is_enabled = poll.is_enabled
                self.polls[poll.poll_id] = poll_obj
                self.received_message_to_poll[poll.received_message] = poll.poll_id
                self.sent_message_to_poll[poll.sent_message] = poll.poll_id

    def add_poll(self, poll: Poll, received_message, sent_message):
        poll.sent_message = sent_message.id
        poll.received_message = received_message.id
        self.polls[poll.poll_id] = poll
        self.sent_message_to_poll[sent_message.id] = poll.poll_id
        self.received_message_to_poll[received_message.id] = poll.poll_id
        self.db.add_poll(poll=poll, received_message=received_message, sent_message=sent_message)

    def update_poll(self, poll: Poll):
        if poll.poll_id in self.polls:
            self.db.update_poll(poll)

    def is_sent_message(self, msg_id: int) -> bool:
        return msg_id in self.sent_message_to_poll

    def is_received_message(self, msg_id: int) -> bool:
        return msg_id in self.received_message_to_poll

    def get_poll_by_id(self, poll_id: str) -> Union[Poll, None]:
        if poll_id in self.polls:
            return self.polls[poll_id]
        else:
            return None

    def get_poll_by_msg_id(self, msg_id: int) -> Union[Poll, None]:
        poll_id = None
        if msg_id in self.sent_message_to_poll:
            poll_id = self.sent_message_to_poll[msg_id]
        elif msg_id in self.received_message_to_poll:
            poll_id = self.received_message_to_poll[msg_id]

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
