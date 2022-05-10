
from IDB import *
from date import today
from DB_enum import TableNames
from DB_types import Column


def save_comment(user_id, comment_value: bool, reliability, stock_name, stock_value):
    now = today()
    if not exists_user(user_id):
        initialize_user(user_id)
    add_object_to_table(TableNames.comments,
                        ("user_id", user_id),
                        ("comment_value", int(comment_value)),
                        ("reliability", reliability),
                        ("stock_name", stock_name),
                        ("stock_value", stock_value),
                        ("date", now)
                        )


def get_user_comments(user_id, days_num):
    time_diff = days_num * 24 * 60 * 60
    now = today()

    requested_values = ["comment_value", "reliability", "stock_name", "stock_value"]
    condition = f"user_id = {user_id} AND date >= {now} - {time_diff}"
    user_comments = get_values(TableNames.comments, requested_values, condition)
    result = []
    for comment in user_comments:
        result.append(tuple(comment))

    return result


def get_users(days_num=None):
    if days_num is not None:
        time_diff = days_num * 24 * 60 * 60
        now = today()
        condition = f"date >= {now} - {time_diff}"
    else:
        condition = "TRUE"

    requested_values = ["user_id"]
    users = get_values(TableNames.comments, requested_values, condition)

    return users


# # when save_comment, must call this
def initialize_user(user_id):
    # initialize points to zero and starting point to zero
    add_object_to_table(TableNames.users,
                        ("user_id", user_id),
                        ("score", 0),
                        ("base_score", 0)
                        )


def set_user_score(user_id, score):
    update_value(TableNames.users, "score", score, f"user_id = {user_id}")


def get_user_score(user_id):
    requested_values = ["score", "base_score"]
    condition = f"user_id = {user_id}"
    user_info = get_values(TableNames.users, requested_values, condition)
    assert len(user_info) <= 1
    if len(user_info) == 1:
        score, user_score = tuple(user_info[0])
        return score, user_score
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
        Column(name="score", type="numeric"),
        Column(name="base_score", type="numeric")       # va messo?
    ]
    crate_table(TableNames.users, "user_id", "int", col_list, autogen=False)


def reset_db():
    delete_all_tables()
    initialize_db()


if __name__ == "__main__":
    # col_list = [
    #     {"name": "product_name", "type": "nvarchar(50)"},
    #     {"name": "price", "type": "int"}
    # ]
    # crate_table("products1", "product_id", "int", col_list)
    # add_object_to_table("products1", column_names=["product_name", "price"], values=["'Tablet'", "1200"])

    # reset_db()
    # save_comment(5, True, 0.057, "Windows", 0.57)
    # print(show_tables())
    # print(get_all_values(TableNames.comments))

    # print(get_user_comments(5, 1))
    # print(get_users(1))
    print(exists_user(1))
    # delete_all_tables()












