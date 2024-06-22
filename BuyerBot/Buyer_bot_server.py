from l2m_windows.get_servers_for_windows import get_all_servers

from web.market import get_all_items_prices

from lists.items_list import get_items_list
from lists.servers_list import get_servers_list
from lists.trash_list import get_trash_list


from main_funs.windows import Windows

import database
import asyncio


items_list = get_items_list()
servers_list = get_servers_list()
trash_list = get_trash_list()

windows = Windows()

minimal_price_for_red = 300
minimal_price_for_purple = 5000


#servers_and_hwnds_list = get_all_servers()

proxy_num = 0


async def main():
    #update_token.update_token()
    #token = get_new_token.get_token()

    while True:
        tasks = []
        for server_id, server_name in servers_list.items():
            market_info = await get_all_items_prices()
            #database.set_jwt_token(token)

            list_of_items = {}
            for server, item_info in market_info.items():
                item_name = item_info[0]
                item_price = item_info[1]

                good = items_list.get('purple').get(item_name)
                if not good:
                    good = items_list.get('red').get(item_name)
                else:
                    purple = True
                if good:
                    list_of_items.update({item_name: int(float(item_price))})

            tasks.append(database.update_prices(list_of_items, server_name))
            #database.update_prices(list_of_items, server_name)

        await asyncio.gather(*tasks)

asyncio.run(main())
