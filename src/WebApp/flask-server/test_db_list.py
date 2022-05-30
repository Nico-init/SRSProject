import json
import sys
from flask import jsonify
sys.path.insert( 0, './src' ) 
from utils.SRS_types import User

with open('./src/WebApp/flask-server/test_db.json', 'r') as db_file:
    db = json.load(db_file)

def get_best_users_global():
    return sorted([User(u['name'], u['at_score'], u['w_score'], 0) for u in db['all_users']], key=lambda u: u.total_score, reverse=True)

def get_best_users_weekly():
    return sorted([User(u['name'], u['at_score'], u['w_score'], 0) for u in db['all_users']], key=lambda u: u.weekly_score, reverse=True)

def get_user(user_id):
    for u in db['all_users']:
        if u['name'] == user_id:
            return User(u['name'], u['at_score'], u['w_score'], 0)
    
    raise Exception("the user does not exist")

def get_user_score_history_weekly(user_id):
    try: return [User(u['name'], u['at_score'], u['w_score'], 0) for u in db['history'][user_id]]
    except: return []


try: print(get_user("vrahsssoss9"))
except Exception as e: print(e)

try: print([u.weekly_score for u in get_user_score_history_weekly("vrahsssoss9")])
except Exception as e: print(e) 