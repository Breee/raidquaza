import sqlalchemy
from sqlalchemy import or_
from utility.globals import LOGGER
from sqlalchemy.orm import sessionmaker
from poll.polls import Poll
import poll.models as poll_models
import datetime
from typing import List
from typing import Union
from database.dbhandler import DbHandler, transaction_wrapper


class PollDBHandler(DbHandler):

    def __init__(self, host, database, port, user, password, dialect, driver):
        super(PollDBHandler, self).__init__(host, database, port, user, password, dialect, driver)
        self.base = poll_models.Base
        self.base.metadata.create_all(self.engine)

    @transaction_wrapper
    def add_poll(self, poll: Poll, received_message, sent_message) -> None:
        new_poll = poll_models.Poll(creation_time=datetime.datetime.now(),
                                    last_update=datetime.datetime.now(),
                                    guild=received_message.guild.id if received_message.guild else None,
                                    channel=received_message.channel.id,
                                    user=received_message.author.id,
                                    received_message=received_message.id,
                                    sent_message=sent_message.id,
                                    poll_id=poll.poll_id,
                                    poll_title=poll.poll_title,
                                    options=poll.options,
                                    reaction_to_option=poll.reaction_to_option,
                                    option_to_reaction=poll.option_to_reaction,
                                    participants=poll.participants,
                                    option_to_participants=poll.option_to_participants,
                                    is_immortal=poll.is_immortal,
                                    is_enabled=poll.is_enabled
                                    )

        self.session.add(new_poll)

    @transaction_wrapper
    def get_poll(self, poll_id: str) -> Union[poll_models.Poll, None]:
        try:
            poll = self.session.query(poll_models.Poll).filter(poll_models.Poll.poll_id == poll_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            LOGGER.warning("Poll with ID %d does not exist" % poll_id)
            return None
        return poll

    @transaction_wrapper
    def get_poll_with_message_id(self, message_id: int) -> Union[poll_models.Poll, None]:
        try:
            poll = self.session.query(poll_models.Poll).filter(
                    or_(poll_models.Poll.sent_message == str(message_id),
                        poll_models.Poll.received_message == str(message_id))).one()
            return poll
        except sqlalchemy.orm.exc.NoResultFound:
            LOGGER.warning("Poll with poll_message or trigger_message ID %d does not exist" % message_id)
        return None

    @transaction_wrapper
    def get_polls(self, age=None) -> List[poll_models.Poll]:
        LOGGER.info(f'Getting polls with age {age}')
        if age:
            since = datetime.datetime.now() - datetime.timedelta(days=age)
            LOGGER.info(f'since: {since}')
            polls = self.session.query(poll_models.Poll).filter(poll_models.Poll.creation_time >= since)
            LOGGER.info(f'polls: {polls}')
        else:
            polls = self.session.query(poll_models.Poll).filter()
        return polls

    @transaction_wrapper
    def update_poll(self, poll: Poll) -> bool:
        old_poll = self.session.query(poll_models.Poll).filter(poll_models.Poll.poll_id == poll.poll_id).one()
        if old_poll:
            old_poll.poll_title = poll.poll_title
            old_poll.options = poll.options
            old_poll.reaction_to_option = poll.reaction_to_option
            old_poll.option_to_reaction = poll.option_to_reaction
            old_poll.participants = poll.participants
            old_poll.option_to_participants = poll.option_to_participants
            old_poll.is_immortal = poll.is_immortal
            return True
        else:
            return False

    @transaction_wrapper
    def disable_poll(self, poll: Poll) -> poll_models.Poll:
        old_poll = self.get_poll(poll.poll_id)
        if old_poll:
            old_poll.last_update = datetime.datetime.now()
            old_poll.enabled = False
            return old_poll

    @transaction_wrapper
    def disable_poll_via_id(self, message_id) -> poll_models.Poll:
        poll = self.get_poll_with_message_id(message_id=message_id)
        if poll:
            poll.last_update = datetime.datetime.now()
            poll.enabled = False
            return poll


if __name__ == '__main__':
    db = PollDBHandler(host="localhost", user="pollman", password="bestpw", port="3307", database="polldb",
                       dialect="mysql", driver="mysqlconnector")
