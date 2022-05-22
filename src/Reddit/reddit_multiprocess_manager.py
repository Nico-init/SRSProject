########################################
#                                      #
#      THIS SCRIPT IS DEPRECATED       #
#                                      #
########################################

from dotenv import dotenv_values
from multiprocessing import Process, Value
from symbol_validation import is_that_a_stock
import sys
import time
import praw
import reticker as rt

sys.path.insert( 0, './src' )   # TRICK TO BE ABLE TO IMPORT sentiment_analysis FROM ANOTHER FOLDER
from ML.sentiment_analysis import sentiment_analysis

TIMEOUT = 600 # 10 minutes (TEMPORARY)
TARGET_SUBREDDIT = "stocks"

def check_for_symbols(c):
    return rt.TickerExtractor().extract(c)
    

def comment_check(reddit, id, num_active_sub_proc):
    print("start to check {} post for comments...".format(id))
    start = time.time()
    num_processed_comments = 0
    while time.time() - start < TIMEOUT:
        sub = reddit.submission(id)
        comment_forest = sub.comments

        if comment_forest.__len__() > num_processed_comments: # IF THERE ARE NEW COMMENTS 
            # FOR SEMPLICITY WE ONLY CONSIDER ONE NEW COMMENT AT MOST
            new_comment = comment_forest[num_processed_comments]
            print("New comment found for this post: {}".format(id))
            print("{}\n\n".format(new_comment.body))
            num_processed_comments += 1

            stock_symbols = check_for_symbols(new_comment.body)     # CHECK FOR STOCK SYMBOLS IN COMMENT
            for symbol in stock_symbols:
                if is_that_a_stock(symbol):
                    body = new_comment.body.replace('$', '')   # REMOVE ALL STOCK PRE-FIXES FOR TARGET COHERENCE
                    analysis_results = sentiment_analysis(body, target=symbol)

                    # CHECK RESULTS
                    # DECIDE WETHER TO SEND THE ENTRY TO THE SCRAPER OR NOT

                    print("Sent an entry for this symbol: {} | with these analysis results: {}".format(stock_symbols, analysis_results)) # TEMPORARY

        time.sleep(1)

    print("Ending process: {}".format(id))
    num_active_sub_proc.value -= 1
    print("\n[[NUMBER OF ACTIVE PROCESSES: {}]]\n".format(num_active_sub_proc.value))
    return


def main():
    config = dotenv_values(r".\src\Reddit\.env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
    
    num_active_sub_proc = Value('i', 0)

    # USING THE PRAW WRAPPER, CREATE A (read-only) REDDIT INSTANCE
    reddit = praw.Reddit(
        client_id=config.get('CLIENT_ID'),
        client_secret=config.get('SECRET'),
        user_agent="getNewPostsBot/0.0.1",
    )

    print("Listening to the subreddit...\n")
    
    for submission in reddit.subreddit(TARGET_SUBREDDIT).stream.submissions(skip_existing=True):
        # check if its advice
        # create multiprocess for comment selection
        # sacrifice a goat to our lord and savior satan
        print("Got a new post...")
 
        if submission.link_flair_text != 'Advice' and submission.link_flair_text != 'Advice Request':
            print("Not an advice post...")
            continue

        print("New advice submission found: {} | {}".format(submission.title, submission.id))
        print("Starting new process for: {}".format(submission.id))
        num_active_sub_proc.value += 1
        print("\n[[NUMBER OF ACTIVE PROCESSES: {}]]\n".format(num_active_sub_proc.value))

        p =  Process(target=comment_check, args=[reddit, submission.id, num_active_sub_proc])
        p.start()
        print("\nListening to the subreddit...\n")


if __name__=="__main__":
    main()



    

    