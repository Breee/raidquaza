import sqlalchemy
from sqlalchemy import or_
from globals.globals import LOGGER
from sqlalchemy.orm import sessionmaker
from poll.poll import Poll
import poll.models as models
import datetime
from typing import List
from typing import Union


def transaction_wrapper(func):
    def _wrap_func(*args, **kwargs):
        self = args[0]
        session = sessionmaker(bind=self.engine, expire_on_commit=False)

        # new session.   no connections are in use.
        self.session = session()
        try:
            # execute transaction statements.
            res = func(*args, **kwargs)
            # commit.  The pending changes above
            # are flushed via flush(), the Transaction
            # is committed, the Connection object closed
            # and discarded, the underlying DBAPI connection
            # returned to the connection pool.
            self.session.commit()
        except Exception as err:
            LOGGER.critical(err)
            # on rollback, the same closure of state
            # as that of commit proceeds.
            self.session.rollback()
            raise
        finally:
            # close the Session.  This will expunge any remaining
            # objects as well as reset any existing SessionTransaction
            # state.  Neither of these steps are usually essential.
            # However, if the commit() or rollback() itself experienced
            # an unanticipated internal failure (such as due to a mis-behaved
            # user-defined event handler), .close() will ensure that
            # invalid state is removed.
            self.session.close()
        return res

    return _wrap_func


class DbHandler(object):

    def __init__(self, host, database, port, user, password, dialect, driver):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.dialect = dialect
        self.driver = driver
        self.conn = None
        self.cursor = None
        self.engine = sqlalchemy.create_engine(
                '%s+%s://%s:%s@%s:%s/%s' % (dialect, driver, user, password, host, port, database), pool_pre_ping=True)
        self.session = None
        self.metadata = sqlalchemy.MetaData()
        self.base = models.Base
        self.base.metadata.create_all(self.engine)

    @transaction_wrapper
    def add_poll(self, poll: Poll) -> None:
        new_poll = models.Poll(creation_time=datetime.datetime.now(),
                               last_update=datetime.datetime.now(),
                               guild=poll.received_message.guild.id,
                               channel=poll.received_message.channel.id,
                               user=poll.received_message.author.id,
                               received_message=poll.received_message.id,
                               sent_message=poll.sent_message.id,
                               poll_id=poll.poll_id,
                               poll_title=poll.poll_title,
                               options=poll.options,
                               reaction_to_option=poll.reaction_to_option,
                               option_to_reaction=poll.option_to_reaction,
                               reactions=poll.reactions,
                               participants=poll.option_to_participants,
                               is_immortal=poll.is_immortal,
                               is_enabled=poll.is_enabled
                               )

        self.session.add(new_poll)

    @transaction_wrapper
    def get_poll(self, poll_id: str) -> Union[models.Poll, None]:
        try:
            poll = self.session.query(models.Poll).filter(models.Poll.poll_id == poll_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            LOGGER.warning("Poll with ID %d does not exist" % poll_id)
            return None
        return poll

    @transaction_wrapper
    def get_poll_with_message_id(self, message_id: int) -> Union[models.Poll, None]:
        try:
            poll = self.session.query(models.Poll).filter(
                    or_(models.Poll.sent_message == str(message_id),
                        models.Poll.received_message == str(message_id))).one()
            return poll
        except sqlalchemy.orm.exc.NoResultFound:
            LOGGER.warning("Poll with poll_message or trigger_message ID %d does not exist" % message_id)
        return None

    @transaction_wrapper
    def get_polls(self, age=None) -> List[models.Poll]:
        LOGGER.info(f'Getting polls with age {age}')
        if age:
            since = datetime.datetime.now() - datetime.timedelta(days=age)
            LOGGER.info(f'since: {since}')
            polls = self.session.query(models.Poll).filter(models.Poll.creation_time >= since)
            LOGGER.info(f'polls: {polls}')
        else:
            polls = self.session.query(models.Poll).filter()
        return polls

    @transaction_wrapper
    def update_poll(self, poll: Poll) -> bool:
        old_poll = self.get_poll(poll.poll_id)
        if old_poll:
            old_poll.guild = poll.received_message.guild.id,
            old_poll.channel = poll.received_message.channel.id,
            old_poll.user = poll.received_message.author.id,
            old_poll.received_message = poll.received_message.id,
            old_poll.sent_message = poll.sent_message.id,
            old_poll.poll_id = poll.poll_id,
            old_poll.poll_title = poll.poll_title,
            old_poll.options = poll.options,
            old_poll.reaction_to_option = poll.reaction_to_option,
            old_poll.option_to_reaction = poll.option_to_reaction,
            old_poll.reactions = poll.reactions,
            old_poll.participants = poll.option_to_participants,
            old_poll.is_immortal = poll.is_immortal
            return True
        else:
            return False

    @transaction_wrapper
    def disable_poll(self, poll: Poll) -> models.Poll:
        old_poll = self.get_poll(poll.poll_id)
        if old_poll:
            old_poll.last_update = datetime.datetime.now()
            old_poll.enabled = False
            return old_poll

    @transaction_wrapper
    def disable_poll_via_id(self, message_id) -> models.Poll:
        poll = self.get_poll_with_message_id(message_id=message_id)
        if poll:
            poll.last_update = datetime.datetime.now()
            poll.enabled = False
            return poll


if __name__ == '__main__':
    db = DbHandler(host="localhost", user="pollman", password="bestpw", port="3307", database="polldb",
                   dialect="mysql", driver="mysqlconnector")
