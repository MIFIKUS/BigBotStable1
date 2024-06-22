from BuyerBot.web.market import get_all_items_prices

import asyncio

import time


async def main():
    while True:
        start = time.time()
        await get_all_items_prices()
        print(time.time()- start)
asyncio.run(main())
