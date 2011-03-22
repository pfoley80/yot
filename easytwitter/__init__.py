import os
import sys
import json
from twitter import Twitter, oauth, oauth_dance

__all__ = ["EasyTwitter", "load_consumer_from_file", "save_consumer_to_file"]

def load_consumer_from_file(path):
   with open(path, "r") as c:
      info = json.loads("\n".join(c.readlines()))
      return info["consumer_key"].encode("utf-8"), info["consumer_secret"].encode("utf-8")

def save_consumer_to_file(path, secret, key):
   with open(path, "wb") as c:
      c.write(json.dumps({"consumer_secret" : secret, "consumer_key" : key}))

class EasyTwitter(object):
   def __init__(self, consumer_uri, token_uri):
      # TODO: deal with storing in a database
      self.consumer_key, self.consumer_secret = load_consumer_from_file(consumer_uri)

      if not os.path.exists(token_uri):
         raise EasyTwitterError(u"Run %s.__init__ manually to authorize this application" % __package__)

      self.token_key, self.token_secret = oauth.read_token_file(token_uri)

      self.twitter = Twitter(
        auth=oauth.OAuth(self.token_key, self.token_secret, self.consumer_key, self.consumer_secret),
        secure=True,
        api_version='1',
        domain='api.twitter.com')

   
   def update(self, status):
      """ Shortcut for posting a status update """

      status = status.encode("utf-8", "replace")
      if len(status) > 140:
         raise EasyTwitterError(u"Status is too long")
      else:
         return self.twitter.statuses.update(status=status)

if __name__ == "__main__":

   if len(sys.argv) < 3:
      print("usage: %s [path to oauth token file] [path to oauth consumer file]" % sys.argv[0])
      print("       The oauth token file will be created for you, but the oauth consumer file must")
      print("       contain valid consumer secret/key")
      sys.exit(1)

   token_uri = sys.argv[1]
   consumer_uri = sys.argv[2]

   if not os.path.exists(token_uri):
      with open(token_uri, "wb") as f:
         pass

   EasyTwitter(consumer_uri, token_uri) 
