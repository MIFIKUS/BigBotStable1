from .headers import HEADERS
from .urls import MAIN_MARKET_URL

from BuyerBot.jwt_updater.fiddler_actions import get_new_token
from BuyerBot.jwt_updater.l2m_actions import update_token
from BuyerBot.jwt_updater.planet_vpn_actions.change_ip import change_ip

from BuyerBot.web.proxy import get_proxy

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_market_info(server_id: int, token: str, proxy_num) -> list:
    proxy = get_proxy(proxy_num)

    HEADERS.update({'Authorization': token})
    data = requests.post(MAIN_MARKET_URL, json={"game_server_id": server_id}, headers=HEADERS, verify=False, proxies=proxy)

    if data.status_code != 200:
        update_token.update_token()
        token = get_new_token.get_token()

        HEADERS.update({'Authorization': token})
        data = requests.post(MAIN_MARKET_URL, json={"game_server_id": server_id}, headers=HEADERS, verify=False, proxies=proxy)

        if data.status_code != 200:
            proxy_num += 1
            proxy = get_proxy(proxy_num)

            #change_ip()
            update_token.update_token()
            token = get_new_token.get_token()

            HEADERS.update({'Authorization': token})
            data = requests.post(MAIN_MARKET_URL, json={"game_server_id": server_id}, headers=HEADERS, verify=False, proxies=proxy)

    return data.json()['list'], token, proxy_num
