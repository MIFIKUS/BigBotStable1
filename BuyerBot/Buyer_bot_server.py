import traceback

from l2m_windows.get_servers_for_windows import get_all_servers

from web.market import get_all_items_prices

from lists.items_list import get_items_list
from lists.servers_list import get_servers_list
from lists.trash_list import get_trash_list


import database
import asyncio


items_list = get_items_list()
servers_list = get_servers_list()
trash_list = get_trash_list()

minimal_price_for_red = 300
minimal_price_for_purple = 5000


#servers_and_hwnds_list = get_all_servers()

proxy_num = 0


async def main():
    #update_token.update_token()
    #token = get_new_token.get_token()

    while True:
        tasks = []
        market_info = await get_all_items_prices()
        #database.set_jwt_token(token)

        print(market_info)

        update_list = {}
        for j in market_info:
            list_of_items = {}
            for i in j:
                for server_id, market_data in i.items():
                    server_name = servers_list.get(server_id)
                    for item_id, item_price in market_data.items():
                        list_of_items.update({item_id: int(float(item_price))})

            update_list.update({server_name: list_of_items})

        database.update_prices(update_list)

        await asyncio.gather(*tasks)

asyncio.run(main())
