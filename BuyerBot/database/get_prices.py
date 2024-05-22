import mysql.connector
from BuyerBot.database.access_data import *


def get_prices(server_id: int):
    query = "SELECT * FROM l2m.items_prices;"
    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True

    cursor = connection.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    print(result)




