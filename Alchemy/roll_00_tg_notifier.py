import telebot
import mysql.connector
import requests

import time
import json


with open('Alchemy\\roll_00_items_ids.json', 'r', encoding='utf-8') as items_ids_json:
    items_ids = json.load(items_ids_json)

with open('Alchemy\\servers_list.json', 'r', encoding='utf-8') as servers_list_json:
    servers_list = json.load(servers_list_json)


TG_USERS_IDS = [420909529]
TG_API_KEY = '7118961031:AAGVl4M5Y0Qhs2Fy42rfEHc3wBhRfl4TdBo'
bot = telebot.TeleBot(TG_API_KEY)

ROLL_00_MINIMAL_PRICE = 100
DELAY = 86_400
COLLECT_PRICE_URL = 'https://ncus1-api.g.nc.com/trade/v1.0/sales/valid/min_unit_price/top'
TG_MSG = ''


def get_jwt_token() -> str:
    host = '31.128.37.77'
    user = 'lineika'
    password = '!Qwertqwert1'

    connection = mysql.connector.connect(host=host, user=user,
                                         password=password)
    connection.autocommit = True
    cursor = connection.cursor()

    query = "SELECT * FROM l2m.bot_data;"
    cursor.execute(query)
    return cursor.fetchall()[0][0]


JWT_TOKEN = get_jwt_token()
HEADERS = {
    "Host": "ncus1-api.g.nc.com",
    "Accept-Encoding": "deflate, gzip",
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json",
    "Accept-Language": "ru-RU",
    "Authorization": JWT_TOKEN,
    "User-Agent": "NCMop/3.18.0 (2555DA2C-0C84-4A6D-A3ED-7383CA112935/5.0.67; Windows; ru-RU; RU)"
}


def prepare_items_list() -> list:
    ready = []
    for i in items_ids.values():
        ready.append({"game_item_key": i['id'], "top": "1", "search": [{"key": "Enchant", "from": i['sharp'], "to": i['sharp']}]})

    data = [ready[i:i + 20] for i in range(0, len(ready), 20)]
    return data


def get_all_prices(server_id: int) -> dict:
    data = {}
    for items in prepare_items_list():
        data_for_request = {"game_server_id": server_id, "game_items": items}
        response = requests.post(COLLECT_PRICE_URL, json=data_for_request, headers=HEADERS, verify=False).json()
        for i in response['list']:
            if i:
                data.update({i['game_item_key']: i['sale_price']})
    return data


def send_msg(msg: str):
    for user in TG_USERS_IDS:
        bot.send_message(user, text=msg, parse_mode='Markdown')


def run():
    TG_MSG = ''
    while True:
        for i in servers_list.items():
            items_prices_info = get_all_prices(i[1])
            amount_of_all_items = len(items_ids)
            amount_of_decent_items = len(list(filter(lambda x: int(x) < ROLL_00_MINIMAL_PRICE, items_prices_info.values())))
            TG_MSG += f'{i[0]}: **({amount_of_decent_items}/{amount_of_all_items})**\n'

        send_msg(TG_MSG)
        time.sleep(DELAY)
