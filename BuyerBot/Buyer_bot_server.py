from l2m_windows.get_servers_for_windows import get_all_servers

from web.market import get_all_items_prices

from lists.items_list import get_items_list
from lists.servers_list import get_servers_list
from lists.trash_list import get_trash_list

from BuyerBot.jwt_updater.l2m_actions import update_token
from BuyerBot.jwt_updater.fiddler_actions import get_new_token

from main_funs.windows import Windows

import database
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
        for server_id, server_name in servers_list.items():
            market_info, token = await get_all_items_prices(token, server_id)
            database.set_jwt_token(token)

            list_of_items = {}
            for i in market_info.items():
                good = items_list.get('purple').get(i[0])
                if not good:
                    good = items_list.get('red').get(i[0])
                else:
                    purple = True
                if good:
                    list_of_items.update({i[0]: int(float(i[1]))})

            database.update_prices(list_of_items, server_name)

asyncio.run(main())
