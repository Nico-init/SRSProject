import requests
from bs4 import BeautifulSoup
import re
from utils.database import *
#kubemq-2.2.4
from kubemq.events import Event
from kubemq.tools.listener_cancellation_token import ListenerCancellationToken
from kubemq.events.subscriber import Subscriber
from kubemq.subscription.subscribe_type import SubscribeType
from kubemq.subscription.events_store_type import EventsStoreType
from kubemq.subscription.subscribe_request import SubscribeRequest

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

def check_stock_name(input):
    result = re.sub(r'[^a-zA-Z.]', '', input)
    return result.upper()

def scrape_value_yahoo(stock_name):
    #Create the url
    url = "https://finance.yahoo.com/quote/" + stock_name
    #Request url page with Requests
    headers={'User-Agent': 'Custom'}
    page = requests.get(url, headers=headers)
    #Finding Stock market price
    soup = BeautifulSoup(page.text, "html.parser")
    fins = soup.find_all("fin-streamer")
    for fin in fins:
        if (fin['data-symbol'] == stock_name and fin['data-field'] == "regularMarketPrice"):
            #Return the stock market price in float
            return float(fin['value'])

def scrape_reddit(event):
    if event:
        print("Subscriber Received Event: Metadata:'%s', Channel:'%s', Body:'%s tags:%s \n" % (
            event.metadata,
            event.channel,
            event.body,
            event.tags
        ))
        #es. event_body = user_id:comment_value:reliability:stock_name:date
        reddit_info = event.body.split(':')
        #scrape stock value
        stock_value = scrape_value_yahoo(check_stock_name(reddit_info[3]))
        #save comment on database
        save_comment(reddit_info[0], reddit_info[1], reddit_info[2], reddit_info[3], stock_value, reddit_info[4])
        #debug
        #print(stock_value)

def handle_incoming_error(error_msg):
    print("received error:%s'" % (
        error_msg
    ))

def main():
    #read from the queue
    channel = 'reddit'
    cancel_token = ListenerCancellationToken()
    try:
        subscriber = Subscriber("localhost:50000")
        subscribe_request = create_subscribe_request(SubscribeType.Events,
                                                     'python-sdk-cookbook-pubsub-events-single-receiver',
                                                     EventsStoreType.Undefined, 0, channel)
        #for each event (reddit info) scrape the value of the stock and save it in the database
        subscriber.subscribe_to_events(subscribe_request, scrape_reddit, handle_incoming_error,
                                       cancel_token)
    except Exception as err:
        print('error, error:%s' % (
            err
        ))

if __name__ == "__main__":
    main()
