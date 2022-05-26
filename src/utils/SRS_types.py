class Comment:
    def __init__(self, comment_id, user_id, comment_value, reliability, stock_name, stock_value, date):
        self.comment_id = comment_id
        self.user_id = user_id
        self.comment_value = comment_value
        self.reliability = reliability
        self.stock_name = stock_name
        self.stock_value = stock_value
        self.date = date

class User:
    def __init__(self, user_id, total_score, weekly_score, base):
        self.user_id = user_id
        self.total_score = total_score
        self.weekly_score = weekly_score
        self.base = base

class Post:
    def __init__(self, post_id, comment_id, start_time, last_update):
        self.post_id = post_id
        self.comment_id = comment_id
        self.start_time = start_time
        self.last_update = last_update
