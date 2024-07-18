import asyncio
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.http import HTTPFlow

import json

class MyAddon:
    def __init__(self):
        pass

    def request(self, flow: HTTPFlow) -> None:
        print("Request Headers:")
        if 'https://ncus1-api.g.nc.com/trade/v1.0/me/sales?' in flow.request.url:
            print(dict(flow.request.headers))
            with open('Autosell\\market_header.json', 'w', encoding='utf-8') as dfdf:
                json.dump(dict(flow.request.headers), dfdf)
            #return flow.request.headers
        #for k, v in flow.request.headers.items():
        #    print(f"{k}: {v}")

    #def response(self, flow: HTTPFlow) -> None:
    #    print("Response Headers:")
    #    for k, v in flow.response.headers.items():
    #        print(f"{k}: {v}")

async def start_proxy():
    opts = options.Options(listen_host='127.0.0.1', listen_port=8080)
    m = DumpMaster(opts, with_termlog=False, with_dumper=False)
    m.addons.add(MyAddon())
    try:
        await m.run()
    except KeyboardInterrupt:
        m.shutdown()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_proxy())