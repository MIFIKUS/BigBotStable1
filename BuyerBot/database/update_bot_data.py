from BuyerBot.database.access_data import *
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
