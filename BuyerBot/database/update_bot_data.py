from database.access_data import *
import mysql.connector


def set_jwt_token(token: str):
    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM l2m.bot_data;')
    prev_token = cursor.fetchall()[0][0]

    query = f"UPDATE l2m.bot_data SET jwt_token = '{token}' WHERE jwt_token = '{prev_token}';"

    cursor.execute(query)

    connection.disconnect()


def set_need_to_update_jwt(is_need: bool):
    if is_need:
        status = 1
    else:
        status = 0

    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True
    cursor = connection.cursor()

    query = f"UPDATE l2m.update_jwt SET need_to_update_jwt = {status} WHERE need_to_update_jwt = {abs(status-1)};"

    cursor.execute(query)

    connection.disconnect()
