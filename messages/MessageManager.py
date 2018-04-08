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

from messages.StoredMessage import StoredMessage
import logging
LOGGER = logging.getLogger('discord')


class MessageManager(object):

    def __init__(self, messages=None):
        # Messages passed shall be a dictionary of the form { command_message_id -> stored message }
        if isinstance(messages, dict):
            self.messages = messages
        elif messages is None:
            self.messages = dict()
        else:
            raise TypeError(
                "The provided messages object is not of type %s, but %s.\n"
                "We expect a dictionary oft the form: { message_ID -> message}" % (dict.__name__, messages))
        self.commandmessage_id_to_storedmessage_id = dict()
        self.postedmessage_id_to_storedmessage_id = dict()
        self.user_to_reportamount = dict()
        self.id_counter = len(self.messages)

    def create_message(self, commandmessage, postedmessage):
        self.id_counter += 1
        stored_message = StoredMessage(id=self.id_counter, commandmessage=commandmessage, postedmessage=postedmessage)
        self.add_message(stored_message)
        self.postedmessage_id_to_storedmessage_id[postedmessage.id] = stored_message.id
        self.commandmessage_id_to_storedmessage_id[commandmessage.id] = stored_message.id
        LOGGER.info("Created StoredMessage #%d, cmd: %s, post: %s" %(self.id_counter, commandmessage.content, postedmessage.content))

    def get_message(self, msg_id=None, commandmessage_id=None, postedmessage_id=None):
        if commandmessage_id and commandmessage_id in self.commandmessage_id_to_storedmessage_id:
            msg_id = self.commandmessage_id_to_storedmessage_id[commandmessage_id]
        elif postedmessage_id and postedmessage_id in self.postedmessage_id_to_storedmessage_id:
            msg_id = self.postedmessage_id_to_storedmessage_id[postedmessage_id]
        if msg_id is not None:
            return self.messages[msg_id]
        else:
            return None

    def add_message(self, message):
        if isinstance(message, StoredMessage):
            self.messages[message.id] = message
        else:
            raise TypeError("parameter message is not of type %s but %s" % (StoredMessage.__name__, message.__class__))

    def delete_message(self, message_id):
        self.messages.pop(message_id, None)

    def restore_messages(self, storage):
        self.messages = storage.messages
        self.commandmessage_id_to_storedmessage_id = storage.commandmessage_id_to_storedmessage_id
        self.postedmessage_id_to_storedmessage_id = storage.postedmessage_id_to_storedmessage_id

    def increase_user_reports(self, user):
        if user in self.user_to_reportamount:
            self.user_to_reportamount[user] += 1
        else:
            self.user_to_reportamount[user] = 1



