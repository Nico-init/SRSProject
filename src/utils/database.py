
from utils.IDB import *
from utils.date import today
from utils.DB_enum import TableNames
from utils.DB_types import Column


class DB_reddit:

    def __init__(self, delete_time):
        """

        :param delete_time: posts older that 'delete_time' will be automatically deleted
        """
        self.delete_time = delete_time

    def save_post(self, post_id: int, comment_id):
        now = today()
        if not self.exists_post(post_id):
            add_object_to_table(TableNames.posts,
                                ("post_id", post_id),
                                ("comment_id", comment_id),
                                ("start_time", now),
                                ("last_update", now)
                                )
        else:
            update_values(TableNames.posts,
                          f"post_id = {post_id}",
                          ("comment_id", comment_id),
                          ("last_update", now)
                          )

    def get_posts(self, time_lapse: int):
        """

        :param time_lapse: it considers only posts which have not been updated last time_lapse seconds
        :return: list of rows which contains a list of values ["post_id", "comment_id", "start_time", "last_update"]
        """

        self.eliminate_old_posts(self.delete_time)
        requested_values = ["post_id", "comment_id", "start_time", "last_update"]
        now = today()
        before_time = now - time_lapse
        condition = f"last_update <= {before_time}"

        user_comments = get_values(TableNames.posts, requested_values, condition)
        return user_comments

    @staticmethod
    def eliminate_old_posts(time: int):
        """
        eliminate posts older than 'time'
        :param time:
        :return:
        """
        now = today()
        delete_time = now - time
        delete(TableNames.posts, f"start_time < {delete_time}")

    @staticmethod
    def exists_post(post_id):
        requested_values = ["post_id"]
        condition = f"post_id = {post_id}"
        result = get_values(TableNames.posts, requested_values, condition)
        return len(result) > 0      # if exists a user, the list of users with user_id will be non-empty


def save_comment(user_id, comment_value: bool, reliability, stock_name, stock_value, date):
    # now = today()
    if not exists_user(user_id):
        initialize_user(user_id)
    add_object_to_table(TableNames.comments,
                        ("user_id", user_id),
                        ("comment_value", int(comment_value)),
                        ("reliability", reliability),
                        ("stock_name", stock_name),
                        ("stock_value", stock_value),
                        ("date", date)
                        )


def get_user_comments(user_id, days_num=None):
    if days_num is not None:
        time_diff = days_num * 24 * 60 * 60
        now = today()
        condition = f"user_id = {user_id} AND date >= {now} - {time_diff}"
    else:
        condition = None

    requested_values = ["comment_id", "user_id", "comment_value", "reliability", "stock_name", "stock_value", "date"]

    user_comments = get_values(TableNames.comments, requested_values, condition, order_by=["date"])
    result = []
    for comment in user_comments:
        result.append(tuple(comment))

    return result


def delete_comment(id_commento):
    condition = f"comment_id = {id_commento}"
    delete(TableNames.comments, condition)


def get_users(days_num=None):
    if days_num is not None:
        time_diff = days_num * 24 * 60 * 60
        now = today()
        condition = f"date >= {now} - {time_diff}"
    else:
        condition = None

    requested_values = ["user_id"]
    users = get_values(TableNames.comments, requested_values, condition, unique=True)

    return users


# # when save_comment, must call this
def initialize_user(user_id):
    # initialize points to zero and starting point to zero
    add_object_to_table(TableNames.users,
                        ("user_id", user_id),
                        ("total_score", 0),
                        ("weekly_score", 0),
                        ("base", 0)
                        )


def set_user_score(user_id, total_score, weekly_score, base):
    if not exists_user(user_id):
        initialize_user(user_id)
    update_values(TableNames.users,
                  f"user_id = {user_id}",
                  ("total_score", total_score),
                  ("weekly_score", weekly_score),
                  ("base", base)
                  )


def get_user_score(user_id):
    requested_values = ["total_score", "weekly_score", "base"]
    condition = f"user_id = {user_id}"
    user_info = get_values(TableNames.users, requested_values, condition)
    assert len(user_info) <= 1
    if len(user_info) == 1:
        total_score, weekly_score, base = tuple(user_info[0])
        return total_score, weekly_score, base
    else:
        raise Exception("the user does not exist")


def exists_user(user_id):
    requested_values = ["user_id"]
    condition = f"user_id = {user_id}"
    result = get_values(TableNames.users, requested_values, condition)
    return len(result) > 0      # if exists a user, the list of users with user_id will be non-empty


def initialize_db():
    col_list = [
        Column(name="user_id", type="int"),
        Column(name="comment_value", type="BIT"),
        Column(name="reliability", type="numeric"),
        Column(name="stock_name", type="nvarchar(50)"),
        Column(name="stock_value", type="numeric"),
        Column(name="date", type="int")
    ]
    crate_table(TableNames.comments, "comment_id", "int", col_list, autogen=True)

    col_list = [
        Column(name="total_score", type="numeric"),
        Column(name="weekly_score", type="numeric"),
        Column(name="base", type="numeric")
    ]
    crate_table(TableNames.users, "user_id", "int", col_list, autogen=False)

    col_list = [
        Column(name="comment_id", type="int"),
        Column(name="start_time", type="int"),
        Column(name="last_update", type="int")
    ]
    crate_table(TableNames.posts, "post_id", "int", col_list, autogen=False)


def reset_db():
    delete_all_tables()
    initialize_db()


def test_database():
    pass
    # reset_db()
    # save_comment(5, True, 0.057, "Windows", 0.57, 125090)
    # print(show_tables())
    # print(get_all_values(TableNames.posts))

    # print(get_user_comments(5))
    # print(get_users())
    # print(exists_user(1))
    # delete_all_tables()
    # set_user_score(2, 9, 10, 7)
    print(get_user_score(2))
    # reddit_db = DB_reddit(100)
    # reddit_db.save_post(7, 2)
    # print(reddit_db.get_posts(10))













