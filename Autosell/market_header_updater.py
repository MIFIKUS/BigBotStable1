from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.http import HTTPFlow

import json
import asyncio


class MyAddon:
    def __init__(self):
        pass

    def request(self, flow: HTTPFlow) -> None:
        if 'https://ncus1-api.g.nc.com/trade/v1.0/me/sales?' in flow.request.url:
            print('Пакет перехвачен')
            server_id = flow.request.url.split('=')[1]
            print(f'Server_id получен {server_id}')

            headers = dict(flow.request.headers)
            print(f'Сырые заголовки {headers}')

            del headers['NCSDK-ReqId']
            del headers['NCSDK-CallbackId']

            headers['server_id'] = server_id

            print(f'Готовые заголовки {headers}')

            with open('AutoSell\\market_header.json', 'w', encoding='utf-8') as market_headers:
                json.dump(headers, market_headers)
                print('Заголовки записаны')


async def start_proxy():
    opts = options.Options(listen_host='127.0.0.1', listen_port=8080)
    m = DumpMaster(opts, with_termlog=False, with_dumper=False)
    m.addons.add(MyAddon())
    try:
        await m.run()
    except KeyboardInterrupt:
        m.shutdown()

def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_proxy())
