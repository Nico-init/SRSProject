import requests
from bs4 import BeautifulSoup
import re
import sys
sys.path.insert( 0, './src' )
from utils.database import *
from utils.comunication import *
from utils.SRS_types import Comment
from builtins import input
from random import randint
from kubemq.events.subscriber import Subscriber
from kubemq.tools.listener_cancellation_token import ListenerCancellationToken
from kubemq.subscription.subscribe_type import SubscribeType
from kubemq.subscription.events_store_type import EventsStoreType
from kubemq.subscription.subscribe_request import SubscribeRequest
import socket
import time

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
        reddit_info = str(event.body.decode("UTF-8")).split(':')
        #print(reddit_info[0])
        #print(isinstance(reddit_info[0], str))
        #scrape stock value
        stock_value = scrape_value_yahoo(check_stock_name(reddit_info[3]))
        #save comment on database
        reddit_info[1] = reddit_info[1]=="positive"
        save_comment(Comment(0, reddit_info[0], reddit_info[1], reddit_info[2], reddit_info[3], stock_value, reddit_info[4]))
        #debug
        print(stock_value)
       

def handle_incoming_error(error_msg):
    print("received error:%s'" % (
        error_msg
    ))

def fake_function(event):
    if event:
        print("Subscriber Received Event: Metadata:'%s', Channel:'%s', Body:'%s tags:%s \n" % (
            event.metadata,
            event.channel,
            event.body,
            event.tags
        ))
    print("fine fake_function")


def main():
    #read from the queue and scrape the value
    print("Subscribing to event on channel testing_event_channel")
    cancel_token=ListenerCancellationToken()

    #Retrieve the kubemw service ip
    ip_server = socket.gethostbyname("kubemq")
    string_connection = ip_server+":"+"50000"
    try:
        # Subscribe to events without store
        #subscriber = Subscriber("10.0.86.232:50000")
        subscriber = Subscriber(string_connection)
        
        print("Creating subscribe request..")
        subscribe_request = SubscribeRequest(
            channel="testing_event_channel",
            #client_id="hello-world-subscriber",
            client_id=socket.gethostname(),
            events_store_type=EventsStoreType.StartFromFirst,
            #events_store_type=EventsStoreType.Undefined,
            events_store_type_value=0,
            group="group1",
            subscribe_type=SubscribeType.EventsStore
        )
        print("Subscribe request created")
        print("Subscribing in progress..")
        #subscriber.subscribe_to_events(subscribe_request, scrape_reddit, handle_incoming_error,cancel_token)
        subscriber.subscribe_to_events(subscribe_request, fake_function, handle_incoming_error,cancel_token)
        print("Scraper subscribed successfully!")
    except Exception as err:
        print('error, error:%s' % (
            err
        ))
    while True:
        time.sleep(0.3)
    #input("Press 'Enter' to stop Listen...\n")
    #cancel_token.cancel()
    #input("Press 'Enter' to stop the application...\n")

if __name__ == "__main__":
    main()
