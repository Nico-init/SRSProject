import datetime
import socket

from kubemq.events.lowlevel.event import Event
from kubemq.events.lowlevel.sender import Sender

if __name__ == "__main__":

    publisher  = Sender("10.0.86.232:50000")
    event = Event(
        metadata="EventMetaData",
        body =("hello kubemq - sending single event").encode('UTF-8'),
        store=False,
        channel="testing_event_channel",
        client_id="hello-world-subscriber"
    )
    try:
        res = publisher.send_event(event)
        print(res)
    except Exception as err:
      print(
            "'error sending:'%s'" % (
                err
                        )
        )