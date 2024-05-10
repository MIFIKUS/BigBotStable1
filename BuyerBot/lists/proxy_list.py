def get_proxy_list() -> str:
    with open('proxy.txt', 'r', encoding='utf-8') as proxy_list:
        return proxy_list.read()
