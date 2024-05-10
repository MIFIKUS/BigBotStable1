import json


def get_items_list() -> dict:
    with open('items_list.json', 'r', encoding='utf-8') as items_list_json:
        return json.load(items_list_json)

