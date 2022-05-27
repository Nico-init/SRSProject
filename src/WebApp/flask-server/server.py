from flask import Flask
import sys
sys.path.insert( 0, './src' ) 
#from utils.database import *

app = Flask(__name__)

@app.route("/all_users")
def users():
    return {"users": [
    {
        "name": "u/giacomino79",
        "w_score" : 300,
        "at_score" : 1496
    },
    {
        "name": "u/vrahsssoss9",
        "w_score" : 246,
        "at_score" : 9762
    },
    {
        "name": "u/pensirenaa",
        "w_score" : 4,
        "at_score" : 2457
    }]}

if __name__ == "__main__":
    app.run(debug=True)
