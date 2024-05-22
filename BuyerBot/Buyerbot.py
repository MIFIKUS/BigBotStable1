from l2m_windows.get_servers_for_windows import get_all_servers
from l2m_windows.get_neccesary_acc_hwnd import get_hwnd_from_list

from web.market import get_market_info, get_all_items_prices
from web.korean_api import get_item_info

from printer.beautifier import BeautifyListofItems
from telegram import sender

from lists.items_list import get_items_list
from lists.servers_list import get_servers_list
from lists.trash_list import get_trash_list

from BuyerBot.jwt_updater.l2m_actions import update_token
from BuyerBot.jwt_updater.fiddler_actions import get_new_token

from main_funs.windows import Windows

from ingame.buy_item import buy_item

import time
import asyncio

items_list = get_items_list()
servers_list = get_servers_list()
trash_list = get_trash_list()

windows = Windows()

minimal_price_for_red = 300
minimal_price_for_purple = 5000


servers_and_hwnds_list = get_all_servers()

proxy_num = 0

async def main():
    update_token.update_token()
    token = get_new_token.get_token()

    while True:
        items_to_research = []
        for server_id, server_name in servers_list.items():
            market_info, token = await get_all_items_prices(token, server_id)
            list_of_items = {}
            for i in market_info.items():
                purple = False
                good = items_list.get('purple').get(i[0])
                if not good:
                    good = items_list.get('red').get(i[0])
                else:
                    purple = True
                if good:
                    list_of_items.update({good: [int(float(i[1])), purple]})

            for item_name, info_list in list_of_items.items():
                price = info_list[0]
                is_purple = info_list[1]
                print(item_name, price)
                if is_purple and price <= minimal_price_for_purple:
                    sender.low_price_notification(item_name, price, server_name, 'purple')
                    hwnd = get_hwnd_from_list(servers_and_hwnds_list, server_name)
                    print(hwnd)
                    windows.open_window_by_hwnd(hwnd)
                    buy_item(item_name, price)
                elif not is_purple and price <= minimal_price_for_red:
                    sender.low_price_notification(item_name, price, server_name, 'red')
                    hwnd = get_hwnd_from_list(servers_and_hwnds_list, server_name)
                    windows.open_window_by_hwnd(hwnd)
                    buy_item(item_name, price)

asyncio.run(main())