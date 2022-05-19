
from utils.IDB import *
from utils.date import today
from utils.DB_enum import TableNames
from utils.DB_types import Column
from utils.DB_naming import Comments, Users, Posts
from utils.types import Comment, User, Post


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
                                (Posts.post_id, post_id),
                                (Posts.comment_id, comment_id),
                                (Posts.start_time, now),
                                (Posts.last_update, now)
                                )
        else:
            update_values(TableNames.posts,
                          f"{Posts.post_id} = {post_id}",
                          (Posts.comment_id, comment_id),
                          (Posts.last_update, now)
                          )

    def get_posts(self, time_lapse: int) -> List[Post]:
        """

        :param time_lapse: it considers only posts which have not been updated last time_lapse seconds
        :return: list of rows which contains a list of Post
        """

        self.eliminate_old_posts(self.delete_time)
        requested_values = [Posts.post_id, Posts.comment_id, Posts.start_time, Posts.last_update]
        now = today()
        before_time = now - time_lapse
        condition = f"{Posts.last_update} <= {before_time}"

        user_comments = [Post(c[0], c[1], c[2], c[3]) for c in get_values(TableNames.posts, requested_values, condition)]
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
        delete(TableNames.posts, f"{Posts.start_time} < {delete_time}")

    @staticmethod
    def exists_post(post_id):
        requested_values = [Posts.post_id]
        condition = f"{Posts.post_id} = {post_id}"
        result = get_values(TableNames.posts, requested_values, condition)
        return len(result) > 0      # if exists a user, the list of users with user_id will be non-empty


def save_comment(user: Comment):
    # now = today()
    if not exists_user(user.user_id):
        initialize_user(user.user_id)
    add_object_to_table(TableNames.comments,
                        (Comments.user_id, user.user_id),
                        (Comments.comment_value, int(user.comment_value)),
                        (Comments.reliability, user.reliability),
                        (Comments.stock_name, user.stock_name),
                        (Comments.stock_value, user.stock_value),
                        (Comments.date, user.date)
                        )


def get_stock_comments(stock_name, days_num=None, since=None) -> List[Comment]:
    """
    for each user that commented a stock, return the last comment
    :param stock_name:
    :param days_num: get all comments more recent that days_num (in number of day)
    :param since: get all comments since that moment (in timetamp: number of seconds since the beginning)
    :return: for each user that commented the stock returns the last Comment
    """
    assert days_num is None or since is None
    if days_num is not None:
        time_diff = days_num * 24 * 60 * 60
        now = today()
        condition = f"{Comments.stock_name} = {stock_name} AND {Comments.date} >= {now} - {time_diff}"
    elif since is not None:
        condition = f"{Comments.stock_name} = {stock_name} AND {Comments.date} >= day"
    else:
        condition = None
    requested_values = [Comments.comment_id, Comments.user_id, Comments.comment_value, Comments.reliability,
                        Comments.stock_name, Comments.stock_value, Comments.date]

    users = {}
    stock_comments = []
    for c in get_values(TableNames.comments, requested_values, condition, order_by=["date"], order_by_asc=False):
        com = Comment(c[0], c[1], c[2], c[3], c[4], c[5], c[6])

        user = com.user_id
        if user not in users:
            users[user] = user
            stock_comments.append(com)

    return stock_comments


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
        now = today()
        condition = f"{Comments.user_id} = {user_id} AND {Comments.date} >= {now} - {time_diff}"
    elif since is not None:
        condition = f"{Comments.user_id} = {user_id} AND {Comments.date} >= day"
    else:
        condition = None

    requested_values = [Comments.comment_id, Comments.user_id, Comments.comment_value, Comments.reliability, Comments.stock_name, Comments.stock_value, Comments.date]

    user_comments = [Comment(c[0], c[1], c[2], c[3], c[4], c[5], c[6]) for c in get_values(TableNames.comments, requested_values, condition, order_by=["date"], order_by_asc=order_by_asc)]

    return user_comments


def delete_comment(id_commento):
    condition = f"{Comments.comment_id} = {id_commento}"
    delete(TableNames.comments, condition)


def get_users(days_num=None):
    """

    :param days_num:
    :return: list of users which made a comment last days_num days (all users id days_num is None
    """
    if days_num is not None:
        time_diff = days_num * 24 * 60 * 60
        now = today()
        condition = f"{Comments.date} >= {now} - {time_diff}"
    else:
        condition = None

    requested_values = [Comments.user_id]
    users = [u[0] for u in get_values(TableNames.comments, requested_values, condition, unique=True)]

    return users


# # when save_comment, must call this
def initialize_user(user_id):
    # initialize points to zero and starting point to zero
    add_object_to_table(TableNames.users,
                        (Users.user_id, user_id),
                        (Users.total_score, 0),
                        (Users.weekly_score, 0),
                        (Users.base, 0)
                        )


def set_user_score(user: User):
    if not exists_user(user.user_id):
        initialize_user(user.user_id)
    update_values(TableNames.users,
                  f"{Users.user_id} = {user.user_id}",
                  (Users.total_score, user.total_score),
                  (Users.weekly_score, user.weekly_score),
                  (Users.base, user.base)
                  )


def get_user(user_id) -> User:
    requested_values = [Users.total_score, Users.weekly_score, Users.base]
    condition = f"{Users.user_id} = {user_id}"
    user_info = get_values(TableNames.users, requested_values, condition)
    assert len(user_info) <= 1
    if len(user_info) == 1:
        total_score, weekly_score, base = tuple(user_info[0])
        return User(user_id, total_score, weekly_score, base)
    else:
        raise Exception("the user does not exist")


def exists_user(user_id):
    requested_values = [Users.user_id]
    condition = f"{Users.user_id} = {user_id}"
    result = get_values(TableNames.users, requested_values, condition)
    return len(result) > 0      # if exists a user, the list of users with user_id will be non-empty


def initialize_db():
    col_list = [
        Column(name=Comments.user_id, type="int"),
        Column(name=Comments.comment_value, type="BIT"),
        Column(name=Comments.reliability, type="numeric"),
        Column(name=Comments.stock_name, type="nvarchar(50)"),
        Column(name=Comments.stock_value, type="numeric"),
        Column(name=Comments.date, type="int")
    ]
    crate_table(TableNames.comments, Comments.comment_id, "int", col_list, autogen=True)

    col_list = [
        Column(name=Users.total_score, type="numeric"),
        Column(name=Users.weekly_score, type="numeric"),
        Column(name=Users.base, type="numeric")
    ]
    crate_table(TableNames.users, Users.user_id, "int", col_list, autogen=False)

    col_list = [
        Column(name=Posts.comment_id, type="int"),
        Column(name=Posts.start_time, type="int"),
        Column(name=Posts.last_update, type="int")
    ]
    crate_table(TableNames.posts, Posts.post_id, "nvarchar(50)", col_list, autogen=False)


def reset_db():
    delete_all_tables()
    initialize_db()


def test_database():
    pass
    # reset_db()
    # save_comment(Comment(4, 5, 0.057, 0.70, "Android", 0.59, today()))
    # print(show_tables())
    # print(get_all_values(TableNames.comments))

    # print([(c.comment_id, c.user_id, c.comment_value, c.reliability, c.stock_name, c.stock_value, c.date)
    #        for c in get_user_comments(5)])
    # print(get_users())
    # print(exists_user(1))
    # delete_all_tables()
    # set_user_score(User(5, 9, 10, 7))
    # print(get_user(2))
    # reddit_db = DB_reddit(100000000000)
    # reddit_db.save_post(7, 2)
    # print(reddit_db.get_posts(10)[0].post_id)
    print(get_stock_comments("Windows"))
    print("hello world")













