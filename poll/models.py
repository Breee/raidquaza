from sqlalchemy import Column, Integer, String, TypeDecorator, TIMESTAMP, Boolean, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class Json(TypeDecorator):
    impl = UnicodeText

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class Poll(Base):
    __tablename__ = 'polls'
    # Overall useful information
    id = Column(Integer, primary_key=True)
    creation_time = Column(TIMESTAMP)
    last_update = Column(TIMESTAMP)
    # Poll information
    guild = Column(String(40))
    channel = Column(String(40))
    user = Column(String(40))
    poll_id = Column(String(255), unique=True)
    poll_title = Column(String(255), unique=True)
    options = Column(Json)
    reaction_to_option = Column(Json)
    option_to_reaction = Column(Json)
    reactions = Column(Json)
    participants = Column(Json)
    option_to_participants = Column(Json)
    sent_message = Column(String(40), unique=True)
    received_message = Column(String(40), unique=True)
    is_immortal = Column(Boolean)
    is_enabled = Column(Boolean)
