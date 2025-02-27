import psycopg2


def esb_conn():
    conn = psycopg2.connect(
        host='localhost',
        database='RGZ',
        user='postgres',
        password='postgres',
        port=5432
    )
    return conn


def check_user(user_id):
    conn = esb_conn()
    curr = conn.cursor()
    curr.execute(f"SELECT COUNT(*) FROM users WHERE id = \'{user_id}\'")
    data = curr.fetchone()
    conn.close()
    return True if data[0] else False


def add_user(user_id, login):
    conn = esb_conn()
    curr = conn.cursor()
    curr.execute(f"INSERT INTO users VALUES ({user_id}, \'{login}\')")
    conn.commit()
    conn.close()


def add_operation(date, amount, chat_id, type):
    conn = esb_conn()
    curr = conn.cursor()
    curr.execute(
        f"INSERT INTO operations (date, sum, chat_id, type_operation) VALUES (\'{date}\', {amount}, \'{chat_id}\', \'{type}\')")
    conn.commit()
    conn.close()


def select_operations(user_id):
    conn = esb_conn()
    curr = conn.cursor()
    curr.execute(f"SELECT date, sum, chat_id, type_operation FROM operations WHERE chat_id = \'{user_id}\'")
    data = curr.fetchall()
    conn.close()
    return data


def get_name(user_id):
    conn = esb_conn()
    curr = conn.cursor()
    curr.execute(f"SELECT name FROM users WHERE id = {user_id}")
    data = curr.fetchone()
    return str(data[0])
