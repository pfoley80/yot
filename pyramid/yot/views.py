# -*- coding: utf-8 -*-

import json
import logging
import transaction

from datetime import datetime, timedelta

from yot.models import DBSession
from yot.models import Event, PullQueueEvent
from yot.event_triggers import triggers

from pyramid.view import view_config

from sqlalchemy import or_, and_

log = logging.getLogger(__name__)

@view_config(renderer='string')
def client_poll(request):
   try:
      recipient = unicode(request.matchdict["recipient"].strip())
   
      # Get all events for this recipient and display as a newline delimited list
      session = DBSession()
      query_results = session.query(PullQueueEvent, Event).filter(
                                    and_(
                                       PullQueueEvent.recipient==recipient, 
                                       PullQueueEvent.event_created==Event.created,
                                       PullQueueEvent.event_sender==Event.sender, 
                                    ))

      results = query_results.all()

      # Save to a list
      def format(result):
         qe, e = result
         return "%s:%s" % (e.type, e.data)

      out = u"total:%i\n%s" % (len(results), "\n".join([format(result) for result in results]))      

      # Remove the results
      session.query(PullQueueEvent).filter(PullQueueEvent.recipient==recipient).delete()

      transaction.commit()

      return out

   except Exception, e:      
      return u"total:0\nerror:%s" % e
   
@view_config(renderer='json')
def client_post(request):
   try:
      event_json = json.loads(request.POST["event"])
      event = Event.from_json(event_json)

      session = DBSession()
      session.add(event)

      session.flush()

      # Run any triggers for this event
      triggers.trigger(event.type, event)

      transaction.commit()

      return {u"status" : u"ok"}
   
   except KeyError, e:
      return {u"param_missing" : unicode(e)}
   except Exception, e:
      return {u"error" : unicode(e)}

@view_config(renderer='json')
def add_event(request):
   # Ideally, the server should know about valid events and be able to present a list
   # and schema for each kind. Then it validates when the human submits an event.
   # For now, we just hardcode this
   try:
      event_json = json.loads(request.POST["event"])
      recipient = request.POST["recipient"]

      session = DBSession()     

      # Add the event and flush it so we can get a reliable primary key
      event = Event.from_json(event_json)      
      session.add(event)  
      session.flush()

      # Create a new command
      command = PullQueueEvent(event, recipient)
      session.add(command)
      session.flush()

      transaction.commit()

      return {u"status" : u"ok"}

   except Exception, e:
      session.rollback()
      return {u"error": unicode(e)}

def main(request): 
    return {"recipients" : ["ddimit"], "sender": "website"}
