from flask import Flask, jsonify
import sys
import json
sys.path.insert( 0, './src' ) 
from utils.database import *

with open('./src/WebApp/flask-server/test_db.json', 'r') as db_file:
    db = json.load(db_file)

app = Flask(__name__)

@app.route("/all_users")
def all_users():
    return {"all_users": db['all_users']}

@app.route("/user/<username>")
def user(username):
    #username = 'u/' + username  #ONLY IF THE REDDIT USERNAMES BEGIN WITH u/, OTHERWISE COMMENT THIS
    for u in db['all_users']:
        if u['name'] == username:
            return u
    return jsonify("None")

if __name__ == "__main__":
    app.run(debug=True)
