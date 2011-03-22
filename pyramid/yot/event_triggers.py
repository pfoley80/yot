from datetime import datetime, timedelta
import functools
import types
import logging

__all__ = ["triggers", "Trigger", "Condition", "ConditionError", "LimitRate"]

log = logging.getLogger(__name__)

class ConditionError(Exception): pass
class Condition(object):
   def __call__(self, trigger, type, event):
      """
      Override this function.
      It should return True if the trigger should run and False if not.
      """

class LimitRate(Condition):
   """ Limits the rate at which a trigger fires """

   def __init__(self, time_limit, now=datetime.utcnow):
      if time_limit is None:
         raise ConditionError(u"time_limit must be given")

      self.now = now
      self.last_time = None
      self.time_limit = timedelta(seconds=time_limit)

   def __call__(self, *args, **kwargs):
      now = self.now()
      result = (self.last_time is None) or (now - self.last_time > self.time_limit)
      self.last_time = now
      return result

class Trigger(object):
   """
   A class that can also be registered as a trigger, for
   when a function is not adequate.
   """

   def __call__(self, type, event, conditions):
      if all([c(self, type, event) for c in conditions]):
         self.trigger(type, event)

   def trigger(self, type, event):
      """ This method will be called for triggering """

class EventTriggers(object):
   def __init__(self):
      self._triggers = {}

   def register(self, event_types, obj, conditions):
      def set_type(type, conditions):      
         if conditions is None:
            conditions = []

         t = self._triggers.setdefault(type, [])   
         t.append({"callable" : obj, "conditions" : conditions})

      def iter_types():
         if isinstance(event_types, str) or isinstance(event_types, unicode):
            set_type(event_types, conditions) 
         else:
            for t in event_types:
               set_type(t, conditions)

      if type(obj) is not types.FunctionType:
         iter_types()
      else: 
         # Use the decorator
         @functools.wraps(obj)
         def wrapper(obj):
            iter_types()
            return obj

         return wrapper            

   def trigger(self, type, event):      
      """ Trigger a trigger. Yo dawg... """

      if type not in self._triggers:
         return False

      for trigger in self._triggers[type]:
         try:          
            log.debug(u"Attempting to execute trigger '%s'" % trigger["callable"])
            trigger["callable"](type=type, event=event, conditions=trigger["conditions"])

         except Exception, e:
            log.error(u"Could not execute trigger '%s': %s" % (trigger["callable"], e))

# Global triggers
triggers = EventTriggers()   
