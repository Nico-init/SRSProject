from builtins import input
from random import randint
from kubemq.events.subscriber import Subscriber
from kubemq.tools.listener_cancellation_token import ListenerCancellationToken
from kubemq.subscription.subscribe_type import SubscribeType
from kubemq.subscription.events_store_type import EventsStoreType
from kubemq.subscription.subscribe_request import SubscribeRequest



def handle_incoming_events(event):
    if event:
        print("Subscriber Received Event: Metadata:'%s', Channel:'%s', Body:'%s tags:%s'" % (
            event.metadata,
            event.channel,
            event.body,
            event.tags
        ))

def handle_incoming_error(error_msg):
        print("received error:%s'" % (
            error_msg
        ))


if __name__ == "__main__":
    print("Subscribing to event on channel example")
    cancel_token=ListenerCancellationToken()


    # Subscribe to events without store
    subscriber = Subscriber("10.0.86.232:50000")
    subscribe_request = SubscribeRequest(
        channel="testing_event_channel",
        client_id="hello-world-subscriber",
        events_store_type=EventsStoreType.Undefined,
        events_store_type_value=0,
        group="",
        subscribe_type=SubscribeType.Events
    )
    subscriber.subscribe_to_events(subscribe_request, handle_incoming_events,handle_incoming_error,cancel_token)

    input("Press 'Enter' to stop Listen...\n")
    cancel_token.cancel()
    input("Press 'Enter' to stop the application...\n")