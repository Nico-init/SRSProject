import sys
sys.path.insert( 0, './src' )

import requests
from bs4 import BeautifulSoup
from utils.database import *
from utils.SRS_types import Comment, User
from datetime import datetime, time, timedelta


#__________________________________________________________________#
#variabili globali
user_comments = []
#alpha for total score
alpha = 0.5
#__________________________________________________________________#

'''
START PRINT FUNCTIONS
'''
def print_comments(list):
    for comment in list:
        print(", ".join([str(c) for c in [comment.user_id, comment.comment_value, comment.reliability, comment.stock_name, comment.date]]))
def print_user(user):
    print("==========USER "+str(user.user_id)+"=================")
    print("Weekly Score: " + str(user.weekly_score))
    print("Total Score: " + str(user.total_score))
    print("Base: " + str(user.base))
'''
END PRINT FUNCTIONS
'''

def scrape_value_yahoo(stock_name):
    """
    :param stock_name: the name of a stock
    :return: value: the uptated stock value
    """
    #Create the url
    url = "https://finance.yahoo.com/quote/" + stock_name
    #Request url page with Requests
    headers={'User-Agent': 'Custom'}
    page = requests.get(url, headers=headers)
    #Finding stock market price
    soup = BeautifulSoup(page.text, "html.parser")
    fins = soup.find_all("fin-streamer")
    for fin in fins:
        if (fin['data-symbol'] == stock_name and fin['data-field'] == "regularMarketPrice"):
            #Return the stock market price in float
            return float(fin['value'])


def get_future_comments_same_stock(stock_name, date):
    """
    :param stock_name: the name of the stock
    :param date: the timestamp of the comment
    :return: list of Comment that are newer than the input date
    """
    #setting variables
    global user_comments
    result = []
    #cycling between the user comments
    for comment in user_comments:
        if (comment.stock_name == stock_name and comment.date > date):
            result.append(comment)
    return result

def check_buysell(comment):
    """
    :param comment
    :return: base: the profit ratio caused by trading
    """
    #setting variables
    global user_comments
    base = 0
    #getting the other comments on the same stock
    future_comments = get_future_comments_same_stock(comment.stock_name, comment.date)
    #print_comments(future_comments)
    if future_comments:
        for future_comment in future_comments:
            if (comment.comment_value): #Positive
                base += ( (future_comment.stock_value - comment.stock_value) * 100 / comment.stock_value ) * comment.reliability
            else: #Negative
                base += ( (comment.stock_value - future_comment.stock_value) * 100 / comment.stock_value ) * comment.reliability
            #delete comment from the local list and delete comment on comments db
            user_comments.remove(comment)
            delete_comment(comment.comment_id)
            #re-iterate if a user has done more than 2 comments on the same stock
            comment = future_comment
    return base

def calculate_profit(comment):
    """
    :param comment
    :return: percentage: the profit ratio
    """
    #scraping the updated stock value from Yahoo Finance
    new_stock_value = scrape_value_yahoo(comment.stock_name)
    #calculating the profit ratio
    percentage = ( (new_stock_value - comment.stock_value) * 100 / comment.stock_value ) * comment.reliability
    #Negative comment case
    if (not comment.comment_value): #Negative
        percentage = -percentage
    #debug
    #print("U: "+comment.user_id+" new: "+str(new_stock_value)+", old: "+str(comment.stock_value)+", mL: "+comment.comment_value+", percentage: "+str(percentage))
    #Update user variables
    return percentage

def get_monday(date):
    """
    :param date: a day in datetime type
    :return: the timestamp of the monday of the 'input date' week
    """
    return datetime.combine((date - timedelta(date.weekday())), time.min).timestamp()

def main():
    global user_comments
    #getting the monday timestamp
    monday = get_monday(datetime.now())
    #getting all the users
    users = get_users()
    #scroll through all the users
    for user_id in users:
        #getting user data
        user = get_user(user_id)
        ## DEBUG:
        print_user(user)
        #setting user variables
        total = 0
        n = 0
        #get user comments
        user_comments.clear()
        user_comments.extend(get_user_comments(user.user_id, since=monday, order_by_asc=True))
        ## DEBUG:
        print_comments(user_comments)
        #Checking if the user has some comments for the week
        if (user_comments):
            #checking if there are some buy/sell for the same stock
            for comment in user_comments:
                user.base += check_buysell(comment)
                #calculating the profit ratio
            for comment in user_comments:
                percentage = calculate_profit(comment)
                if (percentage is not None):
                    total += percentage
                    n += 1
            #updating weekly score
            if (n != 0):
                user.weekly_score = (total + user.base) / n
            else:
                user.weekly_score = 0
        else:
            #updating weekly score
            user.weekly_score = 0

        #updating totale score
        user.total_score = user.total_score * alpha + (1 - alpha) * user.weekly_score
        #save user score on db
        set_user_score(user)
        #save user history
        save_user_history(user)
        ## DEBUG:
        print_user(user)

if __name__ == "__main__":
    main()
