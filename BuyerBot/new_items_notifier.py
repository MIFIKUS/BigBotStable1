from web.market import get_market_info

from web.korean_api import get_item_info

from lists.servers_list import get_servers_list
from lists.items_list import get_items_list
from lists.trash_list import get_trash_list

from telegram import sender

import time

servers_list = get_servers_list()
items_list = get_items_list()['purple']
items_list.update(get_items_list()['red'])

trash_list = get_trash_list()


DELAY = 3600

token = ''

items_to_research = []
while True:
    for server_id, server_name in servers_list.items():
        market_info = get_market_info(int(server_id))

        for i in market_info:
            if not items_list.get(i['group_game_item_key']) and not trash_list.get(i['group_game_item_key']):
                if i['group_game_item_key'] not in items_to_research:
                    items_to_research.append(i['group_game_item_key'])

        print(items_to_research)
        if items_to_research:
            for c in items_to_research:
                print(c)
                item_info = get_item_info(c)
                sender.unknown_item_notification(item_info['item_id'], item_info['item_name'], item_info['img_link'], item_info['color'])

    time.sleep(DELAY)
