from lists.items_list import get_items_list
from database.access_data import *
from database._servers_list import *
import mysql.connector


items_list = get_items_list()
print(items_list)

items_list_to_iterate = items_list['red']
items_list_to_iterate.update(items_list['purple'])


def update_prices(data: dict):
    while True:
        try:
            connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
            connection.autocommit = True
            cursor = connection.cursor()

            print(data)

            full_query = ''

            for server, items in data.items():
                server_column = servers_list.get(server)
                for item_id, item_name in items_list_to_iterate.items():
                    price = items.get(item_id)
                    if price:
                        full_query += f"UPDATE l2m.{server_column} SET price = {price} WHERE item_id = '{item_id}';"
                    else:
                        full_query += f"UPDATE l2m.{server_column} SET price = 0 WHERE item_id = '{item_id}';"

            print(full_query)
            cursor.execute(full_query)
            connection.disconnect()
            break
        except:
            continue
