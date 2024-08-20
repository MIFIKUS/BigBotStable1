import json
#import mysql.connector
#
with open('items_list.json', 'r', encoding='utf-8') as file:
    items = json.load(file)
#connection = mysql.connector.connect(host='31.128.37.77', user='lineika', password='!Qwertqwert1')
#connection.autocommit = True
#cursor = connection.cursor()
#
#
all_items = items['red']; all_items.update(items['purple'])
#
#query = 'DROP TABLE l2m.zighard_global_prices; CREATE TABLE l2m.zighard_global_prices (item_id VARCHAR(255), price INT);'
#for i in all_items.keys():
#    query += f"INSERT IGNORE INTO l2m.zighard_global_prices (item_id, price) VALUES ('{i}', 0); "
#
#cursor.execute(query)
import time

from BuyerBot.main_funs.mouse_and_keboard import AHKActions
from BuyerBot.main_funs.windows import Windows
from BuyerBot.main_funs.images import Image

#ITEMS_IN_2_SLOT = ['Книга Наследника (Увеличение Проворства)']
ITEMS_IN_3_SLOT = ['Алебарда']
ITEMS_IN_2_SLOT = ['Книга Наследника (Увеличение Выносливости)', 'Книга Магии (Восстановление Заклинаний Ⅰ)',
                   'Меч Стража', "Книга Наследника (Сопротивление Оглушению Ⅰ)", "Книга Наследника (Увеличение Мощности Умений Ⅰ)",
                   "Книга Наследника (Решительное Сопротивление Ⅰ)"]
#ITEMS_IN_4_SLOT = ['Книга Наследника (Сопротивление Удержанию)', 'Книга Наследника (Улучшение Оглушения I)']
#ITEMS_IN_5_SLOT = ['Книга Наследника (Увеличение Интеллекта)', ]
#ITEMS_IN_8_SLOT = ['Книга Наследника (Увеличение Мудрости)']
mouse_and_keyboard = AHKActions()
windows = Windows()
image = Image()

def a(item_name):
    def _click_on_item(position):
        if position != 1:
            if position % 2:
                x = 270
                y = 300 + ((position - 3) * 100)
            else:
                x = 1050
            y = 300 + ((position-2) * 100)
        else:
            x = 270
            y = 300
        mouse_and_keyboard.move(x, y, 0)
        mouse_and_keyboard.click()

    position = 1
    if item_name in ITEMS_IN_3_SLOT:
        position = 3
    elif item_name in ITEMS_IN_2_SLOT:
        position = 2

    item_name_for_book = item_name.split(' (')

    if len(item_name_for_book) > 1:
        item_name = '(' + item_name_for_book[-1]

    mouse_and_keyboard.move(800, 290, 0)
    mouse_and_keyboard.click()

    mouse_and_keyboard.move(200, 200, 0)
    mouse_and_keyboard.click()

    mouse_and_keyboard.type(item_name)

    time.sleep(2)
    _click_on_item(position)

for i in all_items.values():
    print(i)
    a(i)
