from dotenv import dotenv_values
from multiprocessing import Process, Value
import sys
import time
import praw
import reticker as rt

# ------------------------------------  Local Imports  ------------------------------------- #
from reddit_utils import is_that_a_stock, base36decode, base36encode
sys.path.insert( 0, './src' ) 
from ML.sentiment_analysis import sentiment_analysis
from utils.database import DB_reddit
from utils.comunication import send
# ------------------------------------------------------------------------------------------ #


# ------------------------------------  Static Params  ------------------------------------- #
DB_CHECK_TIMEOUT = 600 # 10 minutes
DB_POST_TIMEOUT = 100000000000 # temporarily infinite
TARGET_SUBREDDIT = "stocks"
# ------------------------------------------------------------------------------------------ #


# ------------------------------------  DB init  ------------------------------------------- #
reddit_db = DB_reddit(DB_POST_TIMEOUT)
# ------------------------------------------------------------------------------------------ #


def check_for_symbols_and_send(c, username, date):
    """
    :param c: body of comment to analyse

    This method checks a comment's text and retrieves all possible symbols from it.
    It then uses Machine Learning to understand the intentions of the comment for each of 
    the found symbols.
    If any real symbols have been found, it sends all the information to the Scraper.
    """
    print("New comment: {}".format(c))
    possible_symbols = rt.TickerExtractor().extract(c)
    for symbol in possible_symbols:
        if is_that_a_stock(symbol):
            c = c.replace('$', '')   # REMOVE ALL STOCK PRE-FIXES FOR TARGET COHERENCE
            analysis_results = sentiment_analysis(c, target=symbol)
            if (analysis_results[0] > 50):
                comment_value = "positive"
                reliability = analysis_results[0] - 50
                send(user_id=username, comment_value=comment_value, reliability=reliability, stock_name=symbol, date=date)
                print("sending a positive comment by {} for this stock: {}. Reliability: [{}]".format(username, symbol, reliability))
            elif (analysis_results[2] > 50):
                comment_value = "negative"
                reliability = analysis_results[2] - 50
                send(user_id=username, comment_value=comment_value, reliability=reliability, stock_name=symbol, date=date)
                print("sending a negative comment by {} for this stock: {}. Reliability: [{}]".format(username, symbol, reliability))
    
    return


def find_new_posts(reddit):
    """
    :param reddit: instance of reddit API

    This method is used as a parallel process that checks for new advice posts in a specific subreddit
    and saves them in the DB.
    """
    print("Started looking for new posts...\n")
    for submission in reddit.subreddit(TARGET_SUBREDDIT).stream.submissions(skip_existing=True):
        print("Got a new post...")
 
        #if submission.link_flair_text != 'Advice' and submission.link_flair_text != 'Advice Request':
        #    print("Not an advice post...")
        #    continue
        print("Saving new post with id: {}\n".format(submission.id))
        reddit_db.save_post(base36decode(submission.id), 0)
    
    return


def find_and_check_new_comments(reddit):
    """
    :param reddit: instance of reddit API

    This method periodically reads the DB for posts that have not been updated in DB_CHECK_TIMEOUT seconds and checks
    for new comments in each post.
    """

    while True:
        print("Checking stored posts for new comments...")
        posts = reddit_db.get_posts(DB_CHECK_TIMEOUT)
        print("Checking {} posts\n".format(len(posts)))
        for post in posts:
            post_id = base36encode(post.post_id)
            post_instance = reddit.submission(post_id)
            post_instance.comment_sort = "old"
            post_instance.comments.replace_more(limit=0)    # Removes all MoreComments from the forest
            print("Number of total comments: {}".format(post_instance.comments.__len__()))
            print("Last checked comment: {}".format(post.comment_id))

            if post_instance.comments.__len__() > post.comment_id:   # There are new comments
                print("Found new comments for {}".format(post_instance.id))
                for comment in post_instance.comments[post.comment_id:]:
                    check_for_symbols_and_send(comment.body, comment.author.name, comment.created_utc)
            
            reddit_db.save_post(base36decode(post_id), post_instance.comments.__len__())
        time.sleep(60)
    
    return


def main():
    config = dotenv_values(r".\src\Reddit\.env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

    # USING THE PRAW WRAPPER, CREATE A (read-only) REDDIT INSTANCE
    reddit = praw.Reddit(
        client_id=config.get('CLIENT_ID'),
        client_secret=config.get('SECRET'),
        user_agent="getNewPostsBot/0.0.1",
    )

    # Using a new parallel process, start finding new posts
    p =  Process(target=find_new_posts, args=[reddit])
    p.start()

    find_and_check_new_comments(reddit)

    return




if __name__=="__main__":
    main()