from kubemq.events import Event, Sender
from kubemq.tools.listener_cancellation_token import ListenerCancellationToken
from kubemq.events.subscriber import Subscriber
from kubemq.subscription.subscribe_type import SubscribeType
from kubemq.subscription.events_store_type import EventsStoreType
from kubemq.subscription.subscribe_request import SubscribeRequest

#----------------------------------------
channel = 'reddit'
cancel_token = ListenerCancellationToken()
#-----------------------------------------

def create_subscribe_request(
        subscribe_type=SubscribeType.Events, client_id="",
        events_store_type=EventsStoreType.Undefined,
        events_store_type_value=0, channel_name='reddit'

):
    return SubscribeRequest(
        channel=channel_name,
        client_id=client_id,
        events_store_type=events_store_type,
        events_store_type_value=events_store_type_value,
        group="",
        subscribe_type=subscribe_type
    )

def read(handle_event_function, handle_error_function):
    global channel, cancel_token
    #read from the queue
    try:
        subscriber = Subscriber("localhost:50000")
        subscribe_request = create_subscribe_request(SubscribeType.Events,
                                                     'python-sdk-cookbook-pubsub-events-single-receiver',
                                                     EventsStoreType.Undefined, 0, channel)
        #for each event (reddit info) scrape the value of the stock and save it in the database
        subscriber.subscribe_to_events(subscribe_request, handle_event_function, handle_error_function,
                                       cancel_token)
    except Exception as err:
        print('error, error:%s' % (
            err
        ))

def send(user_id, comment_value, reliability, stock_name, date):
    global channel, cancel_token
    sender = Sender("localhost:50000")
    #build the event
    event = Event(
        metadata="reddit-to-scraper",
        body=(""+user_id+":"+comment_value+":"+reliability+":"+stock_name+":"+date).encode('UTF-8'),
        store=False,
        channel=channel,
        client_id="python-sdk-cookbook-pubsub-events-single-sender"
    )
    event.tags = [
        ('key', 'value'),
        ('key2', 'value2'),
    ]
    try:
        sender.send_event(event)
    except Exception as err:
        print('error:%s' % (
            err
        ))
    sleep(5)
    cancel_token.cancel()
