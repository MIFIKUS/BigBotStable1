from BuyerBot.web.headers import KOREAN_API_HEADERS
from BuyerBot.web.urls import KOREAN_L2M_API_URL

import requests


COLORS = {'영웅': 'red', '전설': 'purple', '특수': 'special', '일반': 'grey'}


def get_item_info(item_id) -> dict:
    print(item_id)
    item_id = item_id.replace(' ', '')
    url = KOREAN_L2M_API_URL + str(item_id)
    data = requests.get(url, headers=KOREAN_API_HEADERS, verify=False).json()
    color = COLORS.get(data['grade_name'])
    return {'item_id': item_id, 'item_name': data['item_name'], 'img_link': data['image'], 'color': color}

