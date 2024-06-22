from database.access_data import *
from database._servers_list import *
import mysql.connector


def get_prices(server_name: int):
    server_column = servers_list.get(server_name)

    query = f"SELECT * FROM l2m.{server_column};"
    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True

    cursor = connection.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    items_and_prices = {}

    for item_id, price in result:
        items_and_prices.update({item_id: price})
    return items_and_prices
