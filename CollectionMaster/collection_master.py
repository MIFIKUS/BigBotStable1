from .classes import Windows, AHKActions
from .collect_info.collect_info import CollectInfo
from .functions import MainFunctions, InGameActions
from .config.preferences_for_bot import Preferences

import TGNotifier
import time

functions = MainFunctions()
windows = Windows()
ahk = AHKActions()


class Bot(Preferences):
    def main_cycle(self):
        for scroll_name in self.LIST_OF_SCROLLS:
            print('scroll name', scroll_name)

            no_more_items = False
            no_safe_sharp_collections = False

            while no_more_items is False:
                functions.open_inventory()

                if functions.open_scroll(scroll_name) is False:
                    functions.get_scrolls_from_groccery(scroll_name)
                    continue
                functions.pull_items_in_scroll()
                functions.take_off_equipped_items()

                no_suitable_items = False
                item_sharped = False

                for sharp_lvl in range(1, 11):
                    if item_sharped or no_more_items is True:
                        break
                    no_suitable_items = False

                    list_of_safe_sharp_lvl = []
                    list_of_current_sharp_lvl = []
                    for columns in range(2):
                        if no_suitable_items or item_sharped:
                            break

                        for rows in range(8):
                            if no_suitable_items or item_sharped:
                                break

                            while True:

                                if functions.check_if_slot_empty(columns, rows) is True:
                                    if columns == 0 and rows == 0:
                                        no_more_items = True
                                    no_suitable_items = True
                                    break

                                x = 600 + (95 * rows)
                                y = 450 + (90 * columns)

                                functions.open_item_info(x, y)
                                item_info = CollectInfo()

                                list_of_safe_sharp_lvl.append(item_info.safe_sharp_lvl)
                                list_of_current_sharp_lvl.append(functions.get_item_current_sharp_lvl())

                                print('columuns', columns)
                                print('rows', rows)

                                if item_info.color not in self.suitable_colors:
                                    functions.take_off_item(x, y)
                                    print('Шмотка не подходит из за цвета')
                                    continue

                                if item_info.ready_for_collection:
                                    print('Эту шмотку можно добавить в колу')
                                    functions.add_to_collection()
                                    item_sharped = True
                                    break

                                break

                    if not item_sharped and no_more_items is False:
                        print('list_of_current_sharp_lvl', list_of_current_sharp_lvl)
                        print('list_of_safe_sharp_lvl', list_of_safe_sharp_lvl)
                        print('sharp_lvl', sharp_lvl)
                        if min(list_of_current_sharp_lvl) > sharp_lvl and min(list_of_current_sharp_lvl) >= min(list_of_safe_sharp_lvl):
                            sharp_lvl = min(list_of_current_sharp_lvl)
                            print(f'Текущий минимальный уровень заточки предметов {sharp_lvl}')

                        elif sharp_lvl < min(list_of_safe_sharp_lvl):
                            sharp_lvl = min(list_of_safe_sharp_lvl) - 1

                        if functions.sharp(sharp_lvl) is False:
                            for _ in range(2):
                                ahk.esc()
                                time.sleep(1)

                            functions.get_scrolls_from_groccery(scroll_name)
                            continue
def run():
    try:
        bot = Bot()
        windows.switch_windows(bot.main_cycle)
    except Exception as e:
        TGNotifier.send_break_msg('Колы', '', e)