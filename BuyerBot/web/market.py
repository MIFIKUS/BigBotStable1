import traceback
from typing import List, Dict, Any

from .headers import HEADERS
from .urls import MAIN_MARKET_URL, COLLECT_PRICE_URL

from lists.servers_list import get_servers_list
from lists.items_list import get_items_list

from database.get_bot_data import get_jwt_token
from database.update_bot_data import set_need_to_update_jwt

from aiohttp.client import ClientTimeout

import requests
import urllib3

import aiohttp
import asyncio

import time

DELAY_GET_JWT = 10

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

servers_ids = get_servers_list().keys()
servers_list = get_servers_list()

red_items_list = get_items_list()['red']
purple_items_list = get_items_list()['purple']

red_items_list.update(purple_items_list)


async def get_all_items_prices():
    token = get_jwt_token()
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

    async def fetch_url(data, server_id, session):
        def set_empty() -> list[dict[str, Any]]:
            empty_data = []
            for i in data:
                empty_data.append({'game_item_key': i['game_item_key'], 'sale_price': '0'})
            print('empty')
            return empty_data

        while True:
            try:
                data_for_request = {"game_server_id": server_id, "game_items": data}
                async with session.post(COLLECT_PRICE_URL, json=data_for_request, headers=HEADERS, timeout=ClientTimeout(total=2)) as response:
                    #print(await response.text())
                    if response.status != 200:
                        set_need_to_update_jwt(True)
                        time.sleep(DELAY_GET_JWT)
                        token = get_jwt_token()
                        HEADERS.update({'Authorization': token})

                    return await response.json(), server_id
            except Exception as e:
                traceback.print_exc()
                #session.close()
                return {'list': set_empty()}, server_id

    items_list = _prepare_items_list()
    tasks = []
    async with aiohttp.ClientSession() as session:
        for server_id, server_name in servers_list.items():
            for data in items_list:
                tasks.append(fetch_url(data, server_id, session))
        results = await asyncio.gather(*tasks)

    ready_list = []
    ids_and_prices = {}
    counter = 1

    barc_list = []
    leona_list = []
    zighard_list = []
    erika_list = []

    for result, server in results:
        if result:
            for j in result['list']:
                if j:
                    ids_and_prices.update({j['game_item_key']: j['sale_price']})
        match server:
            case '9001':
                barc_list.append({server: ids_and_prices})
                ids_and_prices = {}
            case '9011':
                zighard_list.append({server: ids_and_prices})
                ids_and_prices = {}
            case '9031':
                leona_list.append({server: ids_and_prices})
                ids_and_prices = {}
            case '9041':
                erika_list.append({server: ids_and_prices})
                ids_and_prices = {}

    all_servers_list = [barc_list, zighard_list, leona_list, erika_list]
    for i in all_servers_list:
        ready_list.append(i)
    return ready_list


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

