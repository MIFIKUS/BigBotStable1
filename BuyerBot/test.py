import requests


HEADERS = {
    "Host": "ncus1-api.g.nc.com",
    "Accept-Encoding": "deflate, gzip",
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json",
    "Accept-Language": "ru-RU",
    "Authorization": 'JWT eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzE1MTk4MTY5IiwiaXNzIjoiMjU1NURBMkMtMEM4NC00QTZELUEzRUQtNzM4M0NBMTEyOTM1IiwiYWNjZXNzX3Rva2VuIjoiNUQ2NkMyOEUtMjBFRi00QTU0LTkzNjYtOEE1M0IxMTg5QUUzIiwidHlwIjoic2Vzc2lvbiJ9.jt7fFHMWUGdTKJImTwsiMy838PIOvUsCxB5IZ1vHXPLHK55MqegEsrGtzZRttEwwokdFy6TKAL1v96Rl3Hyz75f8GObAMnHL8lA7CGHM3WgH9AipaAAlHGb8ujj9Ea6WsZE6EDc9GghnMDe_-It8iGHSLn-Dz0yUsHn3ywrXXxM_6aFp0zfDi1R5sWI02gX7-p9H7yza7J28R3sQWKyRilmC7dzAgGWRspKAdL3Qw2LwdoS0FbPb3TpebXWdoad-QoLRIYijKOcyEBqgfkrBCuC72w5hHYGBWfibm4EJ1C1aIglQwdSyNcD1ph7rqQisMnhjOItJmTnPOaLGnCoeBw',
    "User-Agent": "NCMop/3.18.0 (2555DA2C-0C84-4A6D-A3ED-7383CA112935/5.0.62; Windows; ru-RU; RU)"
}


a = 'https://ncus1-api.g.nc.com/trade/v1.0/market/items/100630002/price'

print(requests.post(a, headers=HEADERS, json={"game_server_id":8033,"game_item_conditions":[{"key":"Enchant","value":0,"type":1}]}).text)