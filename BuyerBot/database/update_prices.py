from lists.items_list import get_items_list
from database.access_data import *
from database._servers_list import *
import mysql.connector


items_list = get_items_list()
print(items_list)

items_list_to_iterate = items_list['red']
items_list_to_iterate.update(items_list['purple'])


async def update_prices(data: dict, server_name):
    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True
    cursor = connection.cursor()

    server_column = servers_list.get(server_name)

    print(data)

    full_query = ''

    for item_id, item_name in items_list_to_iterate.items():
        price = data.get(item_id)
        if price:
            full_query += f"UPDATE l2m.{server_column} SET price = {price} WHERE item_id = '{item_id}';"
        else:
            full_query += f"UPDATE l2m.{server_column} SET price = 0 WHERE item_id = '{item_id}';"

    print(full_query)
    cursor.execute(full_query)
    connection.disconnect()
