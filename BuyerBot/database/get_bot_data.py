from database.access_data import *
import mysql.connector


def get_jwt_token() -> str:
    while True:
        try:
            connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
            connection.autocommit = True
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM l2m.bot_data;')
            return cursor.fetchall()[0][0]
        except Exception:
            pass


def need_to_update_jwt() -> bool:
    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM l2m.update_jwt;')
    return bool(cursor.fetchall()[0][0])

