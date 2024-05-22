from BuyerBot.database.connector import get_cursor
from BuyerBot.lists.items_list import get_items_list
from BuyerBot.database.access_data import *
import mysql.connector



connection = mysql.connector.connect(host='31.128.37.77', user='lineika', password='!Qwertqwert1')
connection.autocommit = True


cursor = connection.cursor()
items_list = get_items_list()


items_list_to_iterate = {}

items_list_to_iterate.update(items_list['red'])
items_list_to_iterate.update(items_list['purple'])


for i in items_list_to_iterate.items():
    query = f"INSERT INTO l2m.barc_global_prices (item_id, price) VALUES ('{i[0]}', 0);"
    cursor.execute(query)

