import time

from BuyerBot.main_funs.mouse_and_keboard import AHKActions
from BuyerBot.main_funs.windows import Windows
from BuyerBot.main_funs.images import Image


mouse_and_keyboard = AHKActions()
windows = Windows()
image = Image()


#ITEMS_IN_2_SLOT = ['Книга Наследника (Увеличение Проворства)']
ITEMS_IN_3_SLOT = ['Алебарда']
ITEMS_IN_2_SLOT = ['Книга Наследника (Увеличение Выносливости)', 'Книга Магии (Восстановление Заклинаний Ⅰ)']
#ITEMS_IN_4_SLOT = ['Книга Наследника (Сопротивление Удержанию)', 'Книга Наследника (Улучшение Оглушения I)']
#ITEMS_IN_5_SLOT = ['Книга Наследника (Увеличение Интеллекта)', ]
#ITEMS_IN_8_SLOT = ['Книга Наследника (Увеличение Мудрости)']



def buy_item(item_name: str, price: int) -> bool:
    position = 1

    def _open_menu():
        mouse_and_keyboard.move(1775, 95, 0)
        mouse_and_keyboard.click()

    def _open_market():
        mouse_and_keyboard.move(1775, 340, 0)
        mouse_and_keyboard.click()

    def _open_global_market():
        mouse_and_keyboard.move(1400, 90, 0)
        mouse_and_keyboard.click()

    def _open_all_categories():
        mouse_and_keyboard.move(90, 380, 0)
        mouse_and_keyboard.click()

    def _open_search_area():
        mouse_and_keyboard.move(800, 290, 0)
        mouse_and_keyboard.click()

    def _click_on_search_area():
        mouse_and_keyboard.move(200, 200, 0)
        mouse_and_keyboard.click()

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

    def _buy():
        for _ in range(5):
            mouse_and_keyboard.move(950, 920, 0)
            mouse_and_keyboard.click()

    def _accept_buy():
        for _ in range(5):
            mouse_and_keyboard.move(805, 920, 0)
            mouse_and_keyboard.click()

    if not image.all_categories_opened():
        while not image.menu_opened():
            _open_menu()

        while not image.market_opened():
            _open_market()

        while not image.globaL_market_opened():
            _open_global_market()

        while not image.all_categories_opened():
            _open_all_categories()

    while not image.search_area_opened():
        _open_search_area()

    if item_name in ITEMS_IN_3_SLOT:
        position = 3
    elif item_name in ITEMS_IN_2_SLOT:
        position = 2

    _click_on_search_area()
    item_name_for_book = item_name.split(' (')

    if len(item_name_for_book) > 1:
        item_name = '(' + item_name_for_book[-1]

    mouse_and_keyboard.type(item_name)

    _click_on_item(position)

    current_price = image.get_price()

    book = False
    if '(' in item_name:
        book = True

    if price == current_price:
        mouse_and_keyboard.move(570, 450)
        mouse_and_keyboard.click()

        if not book:
            neccessary_sharp = image.get_cheapest_sharp(price)

            if neccessary_sharp is False:
                return False
            mouse_and_keyboard.move(570, 450 + (120 * neccessary_sharp))
            mouse_and_keyboard.click()

            time.sleep(0.5)
            if image.get_price_in_final_menu(price) is False:
                return False

            for _ in range(3):
                mouse_and_keyboard.move(570, 450)
                mouse_and_keyboard.click()

            _buy()
            _accept_buy()

        else:
            time.sleep(0.5)
            if image.get_price_in_final_menu(price) is False:
                return False

            for _ in range(3):
                mouse_and_keyboard.move(570, 450)
                mouse_and_keyboard.click()

            _buy()
            _accept_buy()

    return True






