from xmlrpc.client import boolean
from flask import Flask, jsonify
import sys
import json
sys.path.insert( 0, './src' ) 
from utils import database
from utils.SRS_types import User
sys.path.insert( 0, './src/WebApp/flask-server' ) 
import test_db_list
from yf_history import get_stock_history

################
LOCAL = False    #USE LOCAL OR AZURE DB
################

with open('./src/WebApp/flask-server/test_db.json', 'r') as db_file:
    db = json.load(db_file)

app = Flask(__name__)

@app.route("/all_users")
def all_users():
    return get_all_users()

@app.route("/user/<username>")
def user(username):
    return get_user_info(username)

@app.route("/stock/<symbol>")
def stock(symbol):
    return get_stock_info(symbol)

@app.route("/stock/<symbol>/history")
def stock_history(symbol):
    return json.dumps(get_stock_history(symbol))

def get_user_info(username):
    try:
        user = test_db_list.get_user(username) if LOCAL else database.get_user(username)
    except Exception: return jsonify("None")
    res = {
        "user": json.dumps(vars(user)),
        "weekly_history": json.dumps(database.get_user_history_score_weekly(username)),
        "total_history": json.dumps(database.get_user_history_score_global(username, 30)),
        "relevant_comments": json.dumps([vars(c) for c in (test_db_list.get_last_user_relevant_comments(username) if LOCAL else database.get_last_user_relevant_comments(username, 10, 30))])
    }
    return jsonify(res)

def get_all_users():
    res = {
        "weekly": json.dumps([vars(u) for u in (test_db_list.get_best_users_weekly() if LOCAL else database.get_best_users_weekly(25))]),
        "total": json.dumps([vars(u) for u in (test_db_list.get_best_users_global() if LOCAL else database.get_best_users_global(25))])
    }   
    return jsonify(res)


def get_stock_info(symbol):
    if not LOCAL:
        comments = database.get_stock_comments(symbol, False, 30)
        if any(comments):
            return json.dumps([[vars(c) for c in s] for s in comments])
        else: return json.dumps([])
    
    return json.dumps([[vars(c) for c in s] for s in test_db_list.get_stock_comments(symbol)])



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
