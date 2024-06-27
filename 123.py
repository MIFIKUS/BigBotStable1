a = {"game_item_key":"100140001","game_item_conditions":[{"key":"Enchant","type":"1","value":"0"}],"min_unit_price":"11.0000","sale_count":"6"}

b = a['game_item_conditions']

for i in b:
    if i['value'] == "0":
        print(123)


#if a['game_item_conditions']['value'] == "0":
#    print(123)