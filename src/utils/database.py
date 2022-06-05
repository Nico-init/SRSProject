
from utils.IDB import clean_value_to_str, DB_Connection
from utils.date import now, today, day_in_sec, get_timestamp_of_monday_morning
from utils.DB_enum import TableNames
from utils.DB_types import Column
from utils.DB_naming import Comments, Users, Posts, History
from utils.SRS_types import Comment, User, Post
from typing import List, Union, Tuple

DB_conn = DB_Connection()

class DB_reddit:

    def __init__(self, delete_time):
        """

        :param delete_time: posts older that 'delete_time' will be automatically deleted
        """
        self.delete_time = delete_time

    def save_post(self, post_id: int, comment_id):
        now_ts = now()
        if not self.exists_post(post_id):
            DB_conn.add_object_to_table(TableNames.posts,
                                        (Posts.post_id, post_id),
                                        (Posts.comment_id, comment_id),
                                        (Posts.start_time, now_ts),
                                        (Posts.last_update, now_ts)
                                        )
        else:
            DB_conn.update_values(TableNames.posts,
                          f"{Posts.post_id} = {post_id}",
                                  (Posts.comment_id, comment_id),
                                  (Posts.last_update, now_ts)
                                  )

    def get_posts(self, time_lapse: int) -> List[Post]:
        """

        :param time_lapse: it considers only posts which have not been updated last time_lapse seconds
        :return: list of rows which contains a list of Post
        """

        self.eliminate_old_posts(self.delete_time)
        requested_values = [Posts.post_id, Posts.comment_id, Posts.start_time, Posts.last_update]
        now_ts = now()
        before_time = now_ts - time_lapse
        condition = f"{Posts.last_update} <= {before_time}"

        user_comments = [Post(c[0], c[1], c[2], c[3]) for c in DB_conn.get_values(TableNames.posts, requested_values, condition)]
        return user_comments

    @staticmethod
    def eliminate_old_posts(time: int):
        """
        eliminate posts older than 'time'
        :param time:
        :return:
        """
        now_ts = now()
        delete_time = now_ts - time
        DB_conn.delete(TableNames.posts, f"{Posts.start_time} < {delete_time}")

    @staticmethod
    def exists_post(post_id):
        requested_values = [Posts.post_id]
        condition = f"{Posts.post_id} = {post_id}"
        result = DB_conn.get_values(TableNames.posts, requested_values, condition)
        return len(result) > 0      # if exists a user, the list of users with user_id will be non-empty


def save_comment(comment: Comment):
    # now = today()
    if not exists_user(comment.user_id):
        initialize_user(comment.user_id)
    DB_conn.add_object_to_table(TableNames.comments,
                                (Comments.user_id, comment.user_id),
                                (Comments.comment_value, int(comment.comment_value)),
                                (Comments.reliability, comment.reliability),
                                (Comments.stock_name, comment.stock_name),
                                (Comments.stock_value, comment.stock_value),
                                (Comments.date, comment.date)
                                )


def get_stock_comments(stock_name, order_by_global: bool, days_num=7) -> List[List[Comment]]:
    """
    for each user that commented a stock, return the last comment
    :param stock_name:
    :param days_num: get all comments more recent that days_num (in number of day)
    :param since: get all comments since that moment (in timetamp: number of seconds since the beginning)
    :return: for each user that commented the stock returns the last Comment
    """
    today_ts = today()

    start_time = today_ts - (days_num - 1) * day_in_sec()
    end_time = today_ts + day_in_sec()
    condition = f"{Comments.stock_name} = '{stock_name}' AND {Comments.date} >= {start_time} AND {Comments.date} < {end_time}"
    requested_values = [Comments.comment_id, Comments.user_id, Comments.comment_value, Comments.reliability,
                        Comments.stock_name, Comments.stock_value, Comments.date]
    requested_values = [f"{TableNames.comments.value}.{val}" for val in requested_values]

    order_by = Users.total_score if order_by_global else Users.weekly_score

    query = f"SELECT {', '.join(requested_values)}, {TableNames.users.value}.{order_by} " \
            f"FROM {TableNames.comments.value} JOIN {TableNames.users.value} " \
            f"ON {TableNames.comments.value}.{Comments.user_id} = {TableNames.users.value}.{Users.user_id} " \
            f"WHERE {condition} " \
            f"ORDER BY {TableNames.users.value}.{order_by}"

    users = {}
    stock_comments_daily = []
    for i in range(days_num):
        stock_comments_daily.append([])
    comments = DB_conn.exec_query(query, show_result=True)
    for c in comments:
        print(c)
        t = c[6]        # c[date]
        n_day = int((t - start_time) / day_in_sec())
        stock_comments_daily[n_day].append(Comment(c[0], c[1], c[2], c[3], c[4], c[5], c[6]))
    return stock_comments_daily


def get_user_comments(user_id, days_num=None, since=None, order_by_asc=True) -> List[Comment]:
    """

    :param user_id:
    :param days_num: get all comments more recent that days_num (in number of day)
    :param since: get all comments since that moment (in timetamp: number of seconds since the beginning)
    :param order_by_asc: order documents by ascending (descending if False)
    :return: a list of Comment (comment_id, user_id, comment_value, reliability, stock_name, stock_value, date)
    """
    assert days_num is None or since is None
    if days_num is not None:
        time_diff = days_num * 24 * 60 * 60
        now_ts = now()
        condition = f"{Comments.user_id} = {clean_value_to_str(user_id)} AND {Comments.date} >= {now_ts} - {time_diff}"
    elif since is not None:
        condition = f"{Comments.user_id} = {clean_value_to_str(user_id)} AND {Comments.date} >= {since}"
    else:
        condition = None

    requested_values = [Comments.comment_id, Comments.user_id, Comments.comment_value, Comments.reliability, Comments.stock_name, Comments.stock_value, Comments.date]

    user_comments = [Comment(c[0], c[1], c[2], c[3], c[4], c[5], c[6]) for c in DB_conn.get_values(TableNames.comments, requested_values, condition, order_by=["date"], order_by_asc=order_by_asc)]

    return user_comments


def delete_comment(id_commento):
    condition = f"{Comments.comment_id} = {id_commento}"
    DB_conn.delete(TableNames.comments, condition)


def get_users(days_num=None):
    """

    :param days_num:
    :return: list of users which made a comment in the last days_num days (all users id days_num is None
    """
    if days_num is not None:
        time_diff = days_num * 24 * 60 * 60
        now_ts = now()
        condition = f"{Comments.date} >= {now_ts} - {time_diff}"
    else:
        condition = None

    requested_values = [Comments.user_id]
    users = [u[0] for u in DB_conn.get_values(TableNames.comments, requested_values, condition, unique=True)]

    return users


# # when save_comment, must call this
def initialize_user(user_id):
    # initialize points to zero and starting point to zero
    try:
        DB_conn.add_object_to_table(TableNames.users,
                                    (Users.user_id, user_id),
                                    (Users.total_score, 0),
                                    (Users.weekly_score, 0),
                                    (Users.base, 0)
                                    )
    except:
        pass


def set_user_score(user: User):
    """
    given an object user it saves all information about the scores in the database
    :param user:
    :return:
    """
    if not exists_user(user.user_id):
        initialize_user(user.user_id)
    DB_conn.update_values(TableNames.users,
                  f"{Users.user_id} = {clean_value_to_str(user.user_id)}",
                          (Users.total_score, user.total_score),
                          (Users.weekly_score, user.weekly_score),
                          (Users.base, user.base)
                          )


def save_user_history(user: User):
    """
    given the state of a user (user id and user scores), it saves that state together with the date of the moment when this function is called
    :param user: user information to save
    :return:
    """
    user.date = now()
    DB_conn.add_object_to_table(TableNames.history,
                                (History.user_id, user.user_id),
                                (History.total_score, user.total_score),
                                (History.weekly_score, user.weekly_score),
                                (History.base, user.base),
                                (History.date, user.date)
                                )


def get_user_history_score_weekly(user_id):
    """

    :param user_id:
    :return: a list of User objects containing the scores of a user, one for each day and starting from monday
    """
    condition = f"{History.user_id} = {clean_value_to_str(user_id)} AND {History.date} >= {get_timestamp_of_monday_morning()}"

    requested_values = [History.user_id, History.total_score, History.weekly_score, History.base, History.date]
    users = [User(u[0], u[1], u[2], u[3], u[4]) for u in
             DB_conn.get_values(TableNames.history, requested_values, condition, order_by=[History.date], order_by_asc=True)]
    scores = [{"x": u.date * 1000, "y": u.weekly_score} for u in users]
    return scores


def get_user_history_score_global(user_id, days_limit: int):
    """
    :param user_id:
    :param days_limit: number of days considered
    :return: a list of User objects containing the scores of a user, one for each day and starting from days_limit days ago
    """
    condition = f"{History.user_id} = {clean_value_to_str(user_id)} AND {History.date} >= {today() - days_limit * day_in_sec()}"

    requested_values = [History.user_id, History.total_score, History.weekly_score, History.base, History.date]
    users = [User(u[0], u[1], u[2], u[3], u[4]) for u in
             DB_conn.get_values(TableNames.history, requested_values, condition, order_by=[History.date], order_by_asc=True)]
    scores = [{"x": u.date * 1000, "y": u.total_score} for u in users]
    return scores


def get_last_user_relevant_comments(user_id, num_of_elements: int, days_num=7):
    """
    return only the last comment per stock name, written by a user_id
    :param user_id:
    :param num_of_elements:
    :param days_num:
    :return:
    """
    comments = get_user_comments(user_id, days_num, order_by_asc=False)
    unique_comments_per_stock = {}
    # fill unique_comments_per_stock with the first comment per stock
    for c in comments:
        if c.stock_name not in unique_comments_per_stock:
            unique_comments_per_stock[c.stock_name] = c
        if len(unique_comments_per_stock) >= num_of_elements:
            break
    return list(unique_comments_per_stock.values())


def get_best_users_weekly(num_of_users: int):
    """

    :param num_of_users:
    :return: list of best users according to their score weekly
    """
    return get_best_users(num_of_users, order_by_weekly=True)


def get_best_users_global(num_of_users: int):
    """

    :param num_of_users:
    :return:  list of best users according to their score global
    """
    return get_best_users(num_of_users, order_by_weekly=False)


def get_best_users(num_of_users: int, order_by_weekly: bool):
    order_by = [Users.weekly_score] if order_by_weekly else [Users.total_score]

    requested_values = [Users.user_id, Users.total_score, Users.weekly_score, Users.base]

    users = [User(u[0], u[1], u[2], u[3]) for u in DB_conn.get_values(TableNames.users, requested_values, order_by=order_by, order_by_asc=False)]
    return users[:num_of_users]



def get_user(user_id) -> User:
    requested_values = [Users.total_score, Users.weekly_score, Users.base]
    condition = f"{Users.user_id} = {clean_value_to_str(user_id)}"
    user_info = DB_conn.get_values(TableNames.users, requested_values, condition)
    assert len(user_info) <= 1
    if len(user_info) == 1:
        total_score, weekly_score, base = tuple(user_info[0])
        return User(user_id, total_score, weekly_score, base)
    else:
        raise Exception("the user does not exist")


def exists_user(user_id):
    requested_values = [Users.user_id]
    condition = f"{Users.user_id} = {clean_value_to_str(user_id)}"
    result = DB_conn.get_values(TableNames.users, requested_values, condition)
    return len(result) > 0      # if exists a user, the list of users with user_id will be non-empty


def initialize_db():
    col_list = [
        Column(name=Comments.user_id, type="nvarchar(50)"),
        Column(name=Comments.comment_value, type="BIT"),
        Column(name=Comments.reliability, type="real"),
        Column(name=Comments.stock_name, type="nvarchar(50)"),
        Column(name=Comments.stock_value, type="real"),
        Column(name=Comments.date, type="real")
    ]
    DB_conn.crate_table(TableNames.comments, Comments.comment_id, "int", col_list, autogen=True)

    col_list = [
        Column(name=Users.total_score, type="real"),
        Column(name=Users.weekly_score, type="real"),
        Column(name=Users.base, type="real")
    ]
    DB_conn.crate_table(TableNames.users, Users.user_id, "nvarchar(50)", col_list, autogen=False)

    col_list = [
        Column(name=Posts.comment_id, type="int"),
        Column(name=Posts.start_time, type="real"),
        Column(name=Posts.last_update, type="real")
    ]
    DB_conn.crate_table(TableNames.posts, Posts.post_id, "int", col_list, autogen=False)

    col_list = [
        Column(name=History.user_id, type="nvarchar(50)"),
        Column(name=History.total_score, type="real"),
        Column(name=History.weekly_score, type="real"),
        Column(name=History.base, type="real"),
        Column(name=History.date, type="real")
    ]
    DB_conn.crate_table(TableNames.history, History.history_id, "int", col_list, autogen=True)


def reset_db():
    """
    delete all tables amd reset them.
    :return:
    """
    DB_conn.delete_all_tables()
    initialize_db()


def test_database():
    pass
    # save_comment(Comment(4, "pippo_5", True, 0.798, "AAPL", 15.5912345, now() - day_in_sec()))
    # print(show_tables())
    # print(now())
    # print(today())
    # print(len([c[6] for c in DB_conn.get_all_values(TableNames.comments) if c[6] <= today() and c[6] >= today() - 2 * day_in_sec()]))
    # print(DB_conn.get_all_values(TableNames.users))
    # import time
    # start = time.time()
    # for i in range(1000):
    #     h = get_user_comments("_BaldyLocks_", 100)
    #     if i % 1000 == 0:
    #         print(i)
    # print(f"time = {time.time() - start}")
    # print(exists_user("mgmt_professor"))

    # print([(c.comment_id, c.user_id, c.comment_value, c.reliability, c.stock_name, c.stock_value, c.date)
    #        for c in get_user_comments(5)])
    # print(get_users())
    # print(exists_user(1))
    # delete_all_tables()
    # set_user_score(User("pippo1", 9, 10, 7))
    # print(get_user(2))
    # reddit_db = DB_reddit(100000000000)
    # reddit_db.save_post(7, 2)
    # print(reddit_db.get_posts(10)[0].post_id)
    # print([[[c.user_id, c.comment_value] for c in e] for e in get_stock_comments("AAPL", order_by_global=True)])
    # print("hello world")
    # print([[c.comment_id, c.user_id, c.stock_name, c.comment_value] for c in get_last_user_relevant_comments("Thab-Rudy", 10)])
    # print([[u.user_id, u.weekly_score] for u in get_best_users_weekly(2)])
    # save_user_history(User("pippo1", 9, 1, 7, now()))
    # print( get_user_history_score_global("pippo1", 100))
    # print(get_user_history_score_weekly("pippo1"))

    if __name__ == "__main__":
        test_database()










