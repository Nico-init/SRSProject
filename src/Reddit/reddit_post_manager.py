from dotenv import dotenv_values
from multiprocessing import Process, Value
import time
import praw
import sys
import reticker as rt

TIMEOUT = 120 # 2 minutes (TEMPORARY)
TARGET_SUBREDDIT = "stocks"

def check_for_symbol(c):
    # FOR SEMPLICITY WE DONT CHECK IF THE SYMBOL EXISTS
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
            #print("{}\n\n".format(new_comment.body))
            num_processed_comments += 1

            stock_symbols = check_for_symbol(new_comment.body) # CHECK FOR STOCK SYMBOLS IN COMMENT
            if stock_symbols:
                # SEND TO ML FOR INTENT EVALUATION
                # SEND TO SCRAPER
                print("Sent comment with these symbols: {}".format(stock_symbols)) # NEEDS CROSS-VALIDATION WITH OFFICIAL SYMBOLS LIST

        time.sleep(1)

    print("Ending process: {}".format(id))
    num_active_sub_proc.value -= 1
    print("\n[[NUMBER OF ACTIVE PROCESSES: {}]]\n".format(num_active_sub_proc.value))
    return


def main():
    config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
    num_active_sub_proc = Value('i', 0)

    # USING THE PRAW WRAPPER, CREATE A (read-only) REDDIT INSTANCE
    reddit = praw.Reddit(
        client_id=config.get('CLIENT_ID'),
        client_secret=config.get('SECRET'),
        user_agent="getNewPostsBot/0.0.1",
    )

    print("Listening to the subreddit...\n")
    
    process_list = []
    for submission in reddit.subreddit(TARGET_SUBREDDIT).stream.submissions(skip_existing=True):
        # check if its advice
        # create multiprocess for comment selection
        # sacrifice a goat to our lord and savior satan
        print("Got a new post...")

        #if submission.link_flair_text != 'Advice' and submission.link_flair_text != 'Advice Request':
        #    print("Not an advice post...")
        #    continue
        
        # CHECK FOR STOCK SYMBOLS IN COMMENT AND SEND RESULTS (MAYBE FOR LATER IMPLEMENTATION ?)

        print("New advice submission found: {} | {}".format(submission.title, submission.id))
        print("Starting new process for: {}".format(submission.id))
        num_active_sub_proc.value += 1
        print("\n[[NUMBER OF ACTIVE PROCESSES: {}]]\n".format(num_active_sub_proc.value))

        p =  Process(target=comment_check, args=[reddit, submission.id, num_active_sub_proc])
        p.start()
        print("\nListening to the subreddit...\n")


if __name__=="__main__":
    main()



    

    