
import psycopg2

import config.build_config as config


# i'll redo this eventually I guess, consider all of this deprecated for dbnew


def get_cursor():
    dbname = config.read_dbname()
    dbuser = config.read_dbuser()
    dbpass = config.read_dbpass()
    connect_str = "dbname='{}' user='{}' host='localhost' password={}".format(dbname, dbuser, dbpass)
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    return cursor, conn


def get_tasks():
    cursor, connect = get_cursor()
    cursor.execute("""SELECT * from tasks""")
    tasks = cursor.fetchall()
    connect.commit()
    return tasks


def set_tasks(request):
    cursor, connect = get_cursor()
    query = "INSERT INTO tasks VALUES (%s, %s);"
    data = ("crypto", request)
    cursor.execute(query, data)
    connect.commit()


def set_user_stars(user):
    cursor, connect = get_cursor()
    query = "UPDATE USERS SET stars = stars + 1 WHERE id='{}'".format(user)
    cursor.execute(query)
    connect.commit()


def take_user_stars(user):
    cursor, connect = get_cursor()
    query = "UPDATE USERS SET stars = stars - 1 WHERE id='{}'".format(user)
    cursor.execute(query)
    connect.commit()


def get_user_stars(user):
    cursor, connect = get_cursor()
    query = "SELECT stars from USERS where id='{}'".format(user)
    cursor.execute(query)
    stars = cursor.fetchone()[0]
    connect.commit()
    return stars


def set_star():
    cursor, connect = get_cursor()
    query = "UPDATE MEMESTARS SET count = count + 1 WHERE NAME='bot';"
    cursor.execute(query)
    connect.commit()


def get_stars():
    cursor, connect = get_cursor()
    query = "SELECT count from MEMESTARS where name = 'bot'"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return count


def get_user(user: str) -> int:
    cursor, connect = get_cursor()
    query = "SELECT rank from USERS where id='{}'".format(user)
    print(query)

    cursor.execute(query)
    if not cursor.rowcount:
        return False
    rank = cursor.fetchone()[0]
    connect.commit()
    return rank


def set_user(user, role):
    r = get_user(user)
    if r:
        return False
    cursor, connect = get_cursor()
    query = "INSERT INTO USERS VALUES (%s, %s);"
    data = (user, int(role))
    cursor.execute(query, data)
    connect.commit()
    return 1


def set_user_count(user):
    cursor, connect = get_cursor()
    query = "UPDATE USERS SET message_count = message_count + 1 WHERE id='{}'".format(user)
    print(query)
    cursor.execute(query)
    connect.commit()


def set_user_time(age, user):
    cursor, connect = get_cursor()
    query = "UPDATE USERS SET time = time + {} WHERE id='{}'".format(age, user)
    print(query)
    cursor.execute(query)
    connect.commit()


def get_user_time(user):
    cursor, connect = get_cursor()
    query = "SELECT time from USERS where id='{}'".format(user)
    print(query)
    cursor.execute(query)
    time = cursor.fetchone()[0]
    connect.commit()
    return time


def get_user_count(user):
    cursor, connect = get_cursor()
    query = "SELECT message_count from USERS where id='{}'".format(user)
    print(query)
    cursor.execute(query)
    count = cursor.fetchone()[0]
    connect.commit()
    return count


def get_all_users():
    cursor, connect = get_cursor()
    query = "SELECT * FROM USERS"
    cursor.execute(query)
    users = cursor.fetchall()
    print(users)
    return users


def get_users_by_rank(rank):
    cursor, connect = get_cursor()
    query = "SELECT id from USERS where rank>={}".format(rank)
    print(query)
    cursor.execute(query)
    users = cursor.fetchall()
    return users
