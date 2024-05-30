from BuyerBot.database.access_data import *
import mysql.connector


def get_jwt_token() -> str:
    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM l2m.bot_data')
    return cursor.fetchall()[0][0]
