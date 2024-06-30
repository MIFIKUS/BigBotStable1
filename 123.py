import json

with open('Alchemy\\blue_accessory_ids.json', encoding='utf-8') as sdf:
    asdf = json.load(sdf)

aaaa = {}

print("{")
for key, val, in asdf.items():
    print(f'"{val}": "{key}",')

print("}")