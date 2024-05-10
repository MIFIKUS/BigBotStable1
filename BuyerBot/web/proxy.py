from BuyerBot.lists.proxy_list import get_proxy_list


proxy_list = get_proxy_list()


def get_proxy(num) -> dict or bool:
    proxies = proxy_list.split('\n')
    print(proxies)
    if num > len(proxies):
        return False

    necceasary_proxy = proxies[num].split(': ')
    print(necceasary_proxy)

    return {necceasary_proxy[0]: necceasary_proxy[1]}
