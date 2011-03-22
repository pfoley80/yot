# encoding: utf-8

import serial
import datetime
import re
import sys
import time

import twitter_client

class Event(object):
   
   _raw_serial = re.compile("^event:([a-zA-Z0-9_.-])+:(.*)\r\n$")

   def __init__(self, name, data, time=None):
      if time is None:
         self.time = datetime.datetime.utcnow()

      self.name = name
      self.data = data

   def __repr__(self):
      return "<Event:%s %s>" % (self.name, self.time)     

   def data_equal(self, event):
      try:
         return self.data == event.data
      except:
         return False

   def to_status(self):
      return u"%s: The temperature in DDIMIT is %s°C" % (self.time.strftime("%Y-%m-%d %H:%M:%S UTC"), self.data)

   @staticmethod
   def from_serial(line):
      if line is None:
         return None

      match = Event._raw_serial.match(line)

      if match is not None:
         return Event(match.group(1), match.group(2))
      else:
         return None

class Publish(object):
   def __init__(self, interval=300):
      self.interval = datetime.timedelta(seconds=interval)
      self.last_time = datetime.datetime.utcnow()   

      self.last_event = None

   def publish(self, event):
      now = datetime.datetime.utcnow()

      if not event.data_equal(self.last_event):

         if now - self.last_time > self.interval:
            try:
               #print("Publishing to Twitter")
               #twitter_client.update(status=event.to_status())
               self.last_time = now
            except Exception, e:
               print(e)

         print(event.to_status())

      self.last_event = event

def monitor(baudrate, dev):
  
   socket = serial.Serial(baudrate=baudrate, port=dev)
   publisher = Publish(interval=300)  

   def nap():
      time.sleep(1)

   def read():
      line = socket.readline()      
      socket.flush()
      return line

   while True:
      event = Event.from_serial(read())

      if event is not None:      
         publisher.publish(event)
      
      nap()

if __name__ == "__main__":
   def usage():
      print("usage: %s [baudrate] [device]" % sys.argv[0])   
      sys.exit(1)

   if len(sys.argv) < 3:
      usage()
     
   try:
      baudrate = int(sys.argv[1])
      dev = sys.argv[2]   
   except:
      usage()

   monitor(baudrate, dev)
