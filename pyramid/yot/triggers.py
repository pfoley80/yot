import os
from yot.event_triggers import triggers, Trigger, LimitRate
from yot.easytwitter import EasyTwitter

class TwitterTrigger(Trigger):
   def __init__(self, consumer_path, token_path):
      self.twitter = EasyTwitter(consumer_path, token_path)
   
   def trigger(self, type, event):
      s = "On %s UTC, the temperature in DDIMIT was %s degrees" % (event.created.strftime("%Y-%m-%d %H:%M:%S"), event.data)
      self.twitter.update(s)
      
def initialize_triggers(global_config, **settings):
   consumer_path = os.path.join(global_config["here"], "twitter_keys", "consumer.oauth")
   token_path = os.path.join(global_config["here"], "twitter_keys", "token.oauth")

   # Post on Twitter at most every 15 minutes
   triggers.register(
         "TEMPERATURE",
         TwitterTrigger(consumer_path, token_path),         
         [LimitRate(900)])
