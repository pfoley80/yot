import transaction
import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.schema import ForeignKeyConstraint

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# All events
class Event(Base):
   __tablename__ = "events"

   sender = Column(Unicode(255), primary_key=True)   
   created = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)

   type = Column(Unicode(255))
   data = Column(Unicode(4096))
 
   @staticmethod
   def from_json(event_json):
      return Event(type=event_json["type"], sender=event_json["sender"], data=event_json["data"])

   def __init__(self, sender, type, data):
      self.sender = sender
      self.type = type
      self.data = data

# Events to be pulled by the client
class PullQueueEvent(Base):
   __tablename__ = "pull_queue"

   # Map to the proper primary keys
   __table_args__ = (ForeignKeyConstraint(["event_created", "event_sender"], ["events.created","events.sender"]), {})

   event_created = Column(ForeignKey("events.created"), primary_key=True)
   event_sender = Column(ForeignKey("events.sender"), primary_key=True)

   queued = Column(DateTime, default=datetime.datetime.utcnow)
   recipient = Column(Unicode(255)) 

   def __init__(self, event, recipient):
      self.event_created = event.created
      self.event_sender = event.sender
      self.recipient = recipient

def populate():
   pass
    
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        DBSession.rollback()
