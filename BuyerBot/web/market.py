from .headers import HEADERS
from .urls import MAIN_MARKET_URL, COLLECT_PRICE_URL

from BuyerBot.jwt_updater.fiddler_actions import get_new_token
from BuyerBot.jwt_updater.l2m_actions import update_token

from BuyerBot.lists.servers_list import get_servers_list
from BuyerBot.lists.items_list import get_items_list

from BuyerBot.database.get_bot_data import get_jwt_token

from aiohttp.client import ClientTimeout

import requests
import urllib3

import aiohttp
import asyncio


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


servers_ids = get_servers_list().keys()

red_items_list = get_items_list()['red']
purple_items_list = get_items_list()['purple']

red_items_list.update(purple_items_list)

async def get_all_items_prices(token: str, server_id):
    HEADERS.update({'Authorization': token})

    def _prepare_items_list():
        ready = []
        for i in red_items_list.keys():
            if ')' in str(red_items_list.get(i)):
                ready.append({"game_item_key": i, "top": "1", 'search': []})
            else:
                ready.append({"game_item_key": i, "top": "1", "search": [{"key": "Enchant", "from": 0, "to": 11}]})

        data = [ready[i:i + 20] for i in range(0, len(ready), 20)]
        return data

    async def fetch_url(data, token):
        data = {"game_server_id": server_id, "game_items": data}
        while True:
            try:
                async with aiohttp.ClientSession(headers=HEADERS, trust_env=True, timeout=ClientTimeout(total=1)) as session:
                    async with session.post(COLLECT_PRICE_URL, json=data, headers=HEADERS) as response:
                        if response.status != 200:

                            update_token.update_token()
                            token = get_new_token.get_token()

                            HEADERS.update({'Authorization': token})
                        return await response.json(), token
            except Exception:
                continue

    items_list = _prepare_items_list()
    tasks = []
    for data in items_list:
        tasks.append(fetch_url(data, token))
    results = await asyncio.gather(*tasks)

    ids_and_prices = {}
    for result, token in results:
        if result:
            for j in result['list']:
                if j:
                    ids_and_prices.update({j['game_item_key']: j['sale_price']})
    return ids_and_prices, token


def get_market_info(server_id: int) -> list:
    token = get_jwt_token()
    HEADERS.update({'Authorization': token})
    while True:
        try:
            data = requests.post(MAIN_MARKET_URL, json={"game_server_id": server_id}, headers=HEADERS, verify=False)
            break
        except Exception as e:
            print(e)

    return data.json()['list']

