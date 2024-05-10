import json


def get_trash_list() -> dict:
    with open('trash_items.json', 'r', encoding='utf-8') as trash_list_json:
        return json.load(trash_list_json)

