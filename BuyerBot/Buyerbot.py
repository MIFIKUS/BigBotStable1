import time

from l2m_windows.get_servers_for_windows import get_all_servers
from l2m_windows.get_neccesary_acc_hwnd import get_hwnd_from_list

from web.market import get_market_info
from web.korean_api import get_item_info

from printer.beautifier import BeautifyListofItems
from telegram import sender

from lists.items_list import get_items_list
from lists.servers_list import get_servers_list
from lists.trash_list import get_trash_list

from main_funs.windows import Windows

from ingame.buy_item import buy_item


items_list = get_items_list()
servers_list = get_servers_list()
trash_list = get_trash_list()

windows = Windows()

minimal_price_for_red = 300
minimal_price_for_purple = 5000

token = ''

servers_and_hwnds_list = get_all_servers()

proxy_num = 0

while True:
    items_to_research = []
    for server_id, server_name in servers_list.items():
        market_info, token, proxy_num = get_market_info(int(server_id), token, proxy_num)
        list_of_items = {}
        print(market_info)
        for i in market_info:
            purple = False
            good = items_list.get('purple').get(i['group_game_item_key'])

            if not good:
                good = items_list.get('red').get(i['group_game_item_key'])
            else:
                purple = True

            if good:
                list_of_items.update({good: [int(float(i['min_unit_price'])), purple]})
            else:
                if not trash_list.get(i['group_game_item_key']):
                    items_to_research.append(i['group_game_item_key'])


        for item_name, info_list in list_of_items.items():
            price = info_list[0]
            is_purple = info_list[1]
            if is_purple and price <= minimal_price_for_purple:
                hwnd = get_hwnd_from_list(servers_and_hwnds_list, server_name)
                print(hwnd)
                windows.open_window_by_hwnd(hwnd)
                buy_item(item_name, price)

                sender.low_price_notification(item_name, price, server_name, 'purple')

            elif not is_purple and price <= minimal_price_for_red:
                hwnd = get_hwnd_from_list()
                windows.open_window_by_hwnd(hwnd)
                buy_item(item_name, price)

                sender.low_price_notification(item_name, price, server_name, 'red')

    if items_to_research:
        for j in items_to_research:

            item_info = get_item_info(j)
            sender.unknown_item_notification(item_info['item_id'], item_info['item_name'], item_info['img_link'], item_info['color'])
        #beauty_list = BeautifyListofItems(list_of_items)
        #beauty_list.print_beautify_list()


    time.sleep(3)
