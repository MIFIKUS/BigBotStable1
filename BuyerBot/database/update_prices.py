from BuyerBot.database.connector import get_cursor
from BuyerBot.lists.items_list import get_items_list


cursor = get_cursor()
items_list = get_items_list()

items_list_to_iterate = items_list['red'] + items_list['purple']


def update_prices(data: dict):
    list_of_items = []
    for item_id, item_name in items_list_to_iterate.items():
        price = data.get(item_id)
        if price:
            list_of_items.append(f"'{item_id}' = {price}")
        else:
            list_of_items.append(f"'{item_id}' = 0")

    query = f"UPDATE l2m.items_prices SET {",".join(list_of_items)};"
    cursor.execute(query)
