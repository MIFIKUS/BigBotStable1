from BuyerBot.web.market import get_all_items_prices
import asyncio


servers = [9011, 9041, 9001]

async def get_prices():
    tasks = []
    for i in servers:
        tasks.append(get_all_items_prices('JWT eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzE4NTc2NzM2IiwiaXNzIjoiMjU1NURBMkMtMEM4NC00QTZELUEzRUQtNzM4M0NBMTEyOTM1IiwiYWNjZXNzX3Rva2VuIjoiODEyQzIzQUUtNUExQi00OTU5LTg2MjYtMDQ5RThFOEM3RDkxIiwidHlwIjoic2Vzc2lvbiJ9.AC0FOsJagJzGzfwIQEp6VDVun_bLlqmpo4hePM1GoZUtrjnGKLcRbAFolwzk0guNVS38YuD14ZGnzmQm8IXQyQyUKz8CeFbPRW2ZiI3v1B6I5MiNWpXjpxKoy-YfadKpz06wzM9pK5dz29WWBJ3Lhic8rCUm6s0e60oM77VttAgGzlrgmnWjb7GgUp2g49GLLGMH1zk3AdyBVu0al7gTka0NGNXDO5VNdebdTE8KGt_htXp9wst0K_IEh2tPmml7LTAhuwzfFbyYMnm_bBLj9voK-1aQd4uEw-n4RoZQMkyA5xY6wFU4j8QeTEjehQGMG0_KBIPrPd56WZdBMYi-bA',i))
        result = await asyncio.gather(*tasks)
        print(result)
asyncio.run(get_prices())