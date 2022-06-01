from flask import Flask, jsonify
import sys
import json
sys.path.insert( 0, './src' ) 
from utils.database import *
from utils.SRS_types import User
import test_db_list

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

def get_user_info(username):
    try:
        user = test_db_list.get_user(username)
    except Exception: return jsonify("None")
    res = {
        "user": json.dumps(vars(user)),
        "weekly_history": json.dumps([u.weekly_score for u in test_db_list.get_user_score_history_weekly(username)]),
        "total_history": json.dumps([u.total_score for u in test_db_list.get_user_score_history_weekly(username)]),
        "relevant_comments": json.dumps([vars(c) for c in test_db_list.get_last_user_relevant_comments(username)])
    }
    return jsonify(res)

def get_all_users():
    res = {
        "weekly": json.dumps([vars(u) for u in test_db_list.get_best_users_weekly()]),
        "total": json.dumps([vars(u) for u in test_db_list.get_best_users_global()])
    }
    return jsonify(res)


def get_stock_info(symbol):
    return json.dumps([[vars(c) for c in s] for s in test_db_list.get_stock_comments(symbol)])



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
