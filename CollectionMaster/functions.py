from .config.set_path import set_path
from .config.preferences_for_bot import AMOUNT_SCROLLS_TO_TAKE
from .config.groccery_amount_cords import AMOUNT_CORDS
from .classes import Windows, AHKActions, Image
from .errors_handlers import l2m_error_handler as handler
import time

windows = Windows()
ahk = AHKActions()
image = Image()

PATH = set_path()

class InGameActions:
    def open_inventory(self):
        while not handler.is_inventory_opened():
            ahk.press_i()
            time.sleep(2)

        self._set_filter()

    def close_inventory(self):
        while handler.is_inventory_opened():
            ahk.press_i()
            time.sleep(2)

    def _set_filter(self):
        def _open_supplies_menu():
            ahk.move(1340, 450)
            ahk.click()

        def _open_filter_menu():
            ahk.move(1340, 730)
            ahk.click()

        def _switch_entire_row():
            while handler.check_if_filter_seted(0):
                ahk.move(1500, 280)
                ahk.click()

        def _switch_modification_row():
            while not handler.check_if_filter_seted(6, True):
                ahk.move(1500, 750)
                ahk.click()

        def _close_filter_menu():
            ahk.move(1340, 730)
            ahk.click()

        _open_supplies_menu()
        _open_filter_menu()

        _switch_entire_row()
        _switch_modification_row()
        _close_filter_menu()

    def open_item_info(self, x, y):
        ahk.move(x, y)
        ahk.press_mouse()
        time.sleep(2)

    def open_collection_menu(self):
        while not handler.is_collection_menu_opened():
            ahk.move(1550, 745)
            ahk.click()

    def add_item_to_collection(self):
        ahk.move(1640, 950)
        ahk.click()

        ahk.move(960, 670)
        ahk.click()

    def take_off_item(self, x, y):
        ahk.move(x, y)
        ahk.click()
        time.sleep(0.2)

    def pull_items_in_scroll(self):
        def _open_pull_items_menu():
                ahk.move(1700, 830)
                ahk.click()

        def _confirm():
                ahk.move(1600, 830)
                ahk.click()

        _open_pull_items_menu()
        _confirm()

    def click_on_sharp_button(self):
        ahk.move(900, 800)
        ahk.click()

    def agree_unsafe_sharp(self):
        ahk.move(980, 700)
        ahk.click()

    def go_to_town(self):
        def _open_minimap():
            ahk.move(150, 240)
            ahk.click()

        def _click_on_all_locations():
            ahk.move(90, 200)
            ahk.click()

        def _click_on_favourite_locations():
            ahk.move(180, 200)
            ahk.click()

        def _choose_town():
            ahk.move(200, 320)
            ahk.click()

        def _teleport():
            ahk.move(1500, 715)
            ahk.click()

            ahk.move(970, 715)
            ahk.click()

            time.sleep(6)

        _open_minimap()
        time.sleep(3)

        for _ in range(2):
            _click_on_all_locations()
            time.sleep(2)

        _click_on_favourite_locations()
        time.sleep(2)

        _choose_town()
        time.sleep(1)

        _teleport()

    def open_sellers_menu(self):
        ahk.move(350, 280)
        ahk.click()

    def close_sellers_menu(self):
        ahk.move(350, 280)
        ahk.click()

    def return_to_last_location(self):
        def _open_locations():
            ahk.move(350, 180)
            ahk.click()
            time.sleep(1)

        def _choose_location():
            ahk.move(200, 350)
            ahk.click()
            time.sleep(1)

        def _teleport():
            ahk.move(420, 430)
            ahk.click()
            time.sleep(6)

        _open_locations()
        _choose_location()
        _teleport()

    def go_to_groccer(self, x, y):
        ahk.move(x, y)
        ahk.click()
        time.sleep(12)

    def add_scroll(self, x, y):
        for _ in range(2):
            ahk.move(x, y)
            ahk.click()
            time.sleep(0.5)

    def confirm_taking_scrolls(self):
        ahk.move(1610, 950)
        ahk.click()

class ImageActions:
    def _get_equipped_item_cords(self):
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\sharp_menu\\items.png',
                              area_of_screenshot=(550, 375, 1300, 570))

        equipped_items_cords = image.matching(f'{PATH}\\imgs\\screenshots\\sharp_menu\\items.png',
                                        f'{PATH}\\imgs\\templates\\sharp_menu\\equipped.png',
                                         need_for_taking_screenshot=False, threshold=0.7, func=1)

        return equipped_items_cords

    def check_if_slot_empty(self, columns, rows):
        x1 = 555 + (93 * rows)
        x2 = x1 + 105

        y1 = 380 + (95 * columns)
        y2 = y1 + 100

        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\sharp_menu\\is_slot_empty.png',
                              area_of_screenshot=(x1, y1, x2, y2))

        is_slot_empty = image.matching(f'{PATH}\\imgs\\screenshots\\sharp_menu\\is_slot_empty.png',
                          f'{PATH}\\imgs\\templates\\sharp_menu\\empty_slot.png',
                          False, 0.4)

        print('Slot emptyness', is_slot_empty)
        return is_slot_empty

    def detect_red_dot_collection_menu(self):
        time.sleep(4)
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\collection_menu\\collection_menu.png',
                              area_of_screenshot=(670, 260, 1080, 370))

        red_dot_cords = image.matching(f'{PATH}\\imgs\\screenshots\\collection_menu\\collection_menu.png',
                                        f'{PATH}\\imgs\\templates\\collection_menu\\red_dot.png',
                                         need_for_taking_screenshot=False, threshold=0.7, func=1)
        print('red dot_cords = ', red_dot_cords)
        return red_dot_cords

    def find_groccer_cords(self):
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\groccer_menu\\list_of_sellers.png',
                              area_of_screenshot=(45, 150, 100, 530))

        groccer_cords = image.matching(f'{PATH}\\imgs\\screenshots\\groccer_menu\\list_of_sellers.png',
                                      f'{PATH}\\imgs\\templates\\groccer_menu\\logo.png',
                                      need_for_taking_screenshot=False, threshold=0.8, func=1)

        groccer_cords[0] += 50
        groccer_cords[1] += 150
        print('groccer_cords = ', groccer_cords)
        return groccer_cords

    def find_sharp_scrolls_in_groccer_menu(self, scroll_type: str):
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\groccer_menu\\inventory.png',
                              area_of_screenshot=(50, 290, 470, 820))

        scroll_cords = image.matching(f'{PATH}\\imgs\\screenshots\\groccer_menu\\inventory.png',
          f'{PATH}\\imgs\\templates\\sharp_scrolls\\groccer_menu\\{scroll_type.lower()}.png',
                             need_for_taking_screenshot=False, threshold=0.8, func=1)

        scroll_cords[0] += 50
        scroll_cords[1] += 300

        print('scroll_cords = ', scroll_cords)
        return scroll_cords

    def get_item_current_sharp_lvl(self):
        item_name = image.image_to_string(f'{PATH}\\imgs\\screenshots\\item_color.png', False)

        for i in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'):
            if i in item_name:
                return int(i)
        return 0


class MainFunctions(InGameActions, ImageActions):
    def add_to_collection(self):
        def _exit():
            ahk.move(1800, 80)
            ahk.click()
        self.open_collection_menu()
        cords = self.detect_red_dot_collection_menu()

        x = cords[0] + 650
        y = cords[1] + 270

        ahk.move(x, y)
        ahk.click()

        self.add_item_to_collection()

        time.sleep(2)

        _exit()
        time.sleep(2)

    def take_off_equipped_items(self):
        equipped_items_cords = self._get_equipped_item_cords()
        while equipped_items_cords:
            self.take_off_item(600+equipped_items_cords[0], 400+equipped_items_cords[1])

            image.take_screenshot(f'{PATH}\\imgs\\screenshots\\sharp_menu\\items.png',
                                  area_of_screenshot=(550, 375, 1300, 570))

            equipped_items_cords = image.matching(f'{PATH}\\imgs\\screenshots\\sharp_menu\\items.png',
                                                  f'{PATH}\\imgs\\templates\\sharp_menu\\equipped.png',
                                                   need_for_taking_screenshot=False, threshold=0.7, func=1)

    def open_scroll(self, scroll_name):
        def _go_to_multmodification():
            while not handler.is_multimodification_menu_opened():
                ahk.move(1000, 180)
                ahk.click()
                time.sleep(2)

        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\inventory\\inventory.png',
                              area_of_screenshot=(1390, 240, 1800, 775))

        scroll_cords = image.matching(f'{PATH}\\imgs\\screenshots\\inventory\\inventory.png',
                                      f'{PATH}\\imgs\\templates\\sharp_scrolls\\{scroll_name}.png',
                                      need_for_taking_screenshot=False, threshold=0.8, func=1)

        if scroll_cords is False:
            return False

        x = scroll_cords[0] + 1400
        y = scroll_cords[1] + 250

        ahk.move(x, y)

        while not handler.is_modification_menu_opened():
            for _ in range(2):
                ahk.click()
                time.sleep(0.2)
            time.sleep(2)

        time.sleep(2)

        _go_to_multmodification()

    def sharp(self, lvl):
        def _set_sharp_lvl(x, y):
            ahk.move(x, y)
            ahk.click()

        x = 600 + (75 * lvl)
        y = 680

        _set_sharp_lvl(x, y)
        if handler.check_if_enough_scrolls():
            self.click_on_sharp_button()
        else:
            return False

        if handler.need_to_agree_unsafe_sharp():
            self.agree_unsafe_sharp()
        time.sleep(3 * lvl)

    def get_scrolls_from_groccery(self, scroll_type: str):
        self.go_to_town()
        self.open_sellers_menu()

        x, y = self.find_groccer_cords()
        self.go_to_groccer(x, y)

        x, y = self.find_sharp_scrolls_in_groccer_menu(scroll_type)
        self.add_scroll(x, y)

        amount_of_scroll_dict = self._calculate_amount_of_scrolls(AMOUNT_SCROLLS_TO_TAKE)
        self._set_scroll_amount(amount_of_scroll_dict)
        self.confirm_taking_scrolls()

        ahk.esc()
        self.close_sellers_menu()

    def _calculate_amount_of_scrolls(self, amount: int) -> dict:
        if amount % 10:
            raise Exception(f"Колличество свитков должно быть кратно 10! Выбрано {amount}")

        if amount == 2000:
            return {1000: 2}

        if amount == 1500:
            return {1000: 1, 500: 1}

        if amount == 1000:
            return {1000: 1}

        if amount == 500:
            return {100: 5}

        if 100 < amount < 500:
            return {100: amount / 10}

        if amount < 100:
            return {10: amount / 10}

    def _set_scroll_amount(self, instructions: dict):
        for quantity, amount in instructions.items():
            x, y = AMOUNT_CORDS.get(quantity)

            for _ in range(amount):
                ahk.move(x, y)
                ahk.click()
                time.sleep(0.5)