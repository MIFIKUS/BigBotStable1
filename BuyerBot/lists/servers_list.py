import json


def get_servers_list() -> dict:
    with open('servers_list.json', 'r', encoding='utf-8') as servers_list_json:
        return json.load(servers_list_json)

