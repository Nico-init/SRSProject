import requests
from bs4 import BeautifulSoup

class Comment:
    def __init__(self, user_id, stock_name, stock_value, ml_result, reliability, date):
        self.user_id = user_id
        self.stock_name = stock_name
        self.stock_value = stock_value
        self.ml_result = ml_result
        self.reliability = reliability
        self.date = date

class User:
    def __init__(self, user_id, score, starting_point, n_buysell):
        self.user_id = user_id
        self.score = score
        self.starting_point = starting_point
        self.n_buysell = n_buysell
        self.total = 0
        self.n = 0

def mock_all_comments():
    #get all comments from db
    return [
    Comment("ciccio", "AAPL", 130.0, "Positive", 1, 1),
    Comment("marco", "AAPL", 170.0, "Positive", 1, 2),
    Comment("ciccio", "AAPL", 160.0, "Negative", 1, 3),
    Comment("pippo", "AAPL", 140.0, "Negative", 1, 4),
    Comment("pippo", "AAPL", 160.0, "Positive", 1, 5),
    ]


def mock_all_users():
    #get all users from db that have written reddit comments in the interesting period
    return [
    User("ciccio", 0, 0, 0),
    User("pippo", 5, 0, 0),
    User("marco", 3, 0, 0)
    ]


#__________________________________________________________________#
#variabili globali
comments = mock_all_comments()
users = mock_all_users()
#__________________________________________________________________#

def scrape_value_yahoo(stock):
    #Create the url
    url = "https://finance.yahoo.com/quote/" + stock
    #Request url page with Requests
    page = requests.get(url)
    #Finding Stock market price
    soup = BeautifulSoup(page.text, "html.parser")
    fins = soup.find_all("fin-streamer")
    for fin in fins:
        if (fin['data-symbol'] == stock and fin['data-field'] == "regularMarketPrice"):
            #Return the stock market price in float
            return float(fin['value'])

def get_future_comments_same_stock(user, stock_name, date):
    result = []
    for comment in comments:
        if (comment.user_id == user.user_id and comment.stock_name == stock_name and comment.date != date):
            result.append(comment)
    return result

def get_user_stats(user_id):
    for user in users:
        if(user.user_id == user_id):
            return user

def check_buysell(user, comment):
    future_comments = get_future_comments_same_stock(user, comment.stock_name, comment.date)
    if future_comments:
        for future_comment in future_comments:
            if (comment.ml_result == "Positive"):
                user.starting_point += ( (future_comment.stock_value - comment.stock_value) * 100 / comment.stock_value ) * comment.reliability
            elif (comment.ml_result == "Negative"):
                user.starting_point += ( (comment.stock_value - future_comment.stock_value) * 100 / comment.stock_value ) * comment.reliability
            user.n_buysell += 1
            #delete comment from the local list and delete comment on comments db
            comments.remove(comment)
            #re-iterate if a user has done more than 2 comments on the same stock
            comment = future_comment

def calculate_profit(user, comment):
    new_stock_value = scrape_value_yahoo(comment.stock_name)
    percentage = ( (new_stock_value - comment.stock_value) * 100 / comment.stock_value ) * comment.reliability
    #Negative comment case
    if (comment.ml_result == "Negative"):
        percentage = -percentage
    #debug
    print("U: "+comment.user_id+" new: "+str(new_stock_value)+", old: "+str(comment.stock_value)+", mL: "+comment.ml_result+", percentage: "+str(percentage))
    #Update total
    user.total += percentage
    user.n += 1

def main():
    for comment in comments:
        user = get_user_stats(comment.user_id)
        check_buysell(user, comment)
    for comment in comments:
        user = get_user_stats(comment.user_id)
        calculate_profit(user, comment)
    for user in users:
        user.score = (user.total + user.starting_point) / (user.n + user.n_buysell)
        #save_user on db
        print(user.user_id)
        print("Starting Point: " + str(user.starting_point) + ", N: "+str(user.n) + "+" + str(user.n_buysell) +
         "\n Score: " + str(user.score))
        print("-----------------------")
    #debug
    for comment in comments:
        print("- " + comment.user_id + "_" + comment.stock_name + "_" + comment.ml_result + "_" + str(comment.stock_value))


if __name__ == "__main__":
    main()
