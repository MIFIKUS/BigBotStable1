from Booster.Cases import ingame_actions
from Booster.Cases.functions import Checks
from Booster.MainClasses.classes import Windows

import TGNotifier

import time


checks = Checks()
windows = Windows()

FIRST_SLOT_INVENTORY_CORDS = [1440, 290]
SECOND_SLOT_INVENTORY_CORDS = [1540, 290]

def main():
    try:
        ingame_actions.open_inventory()
        ingame_actions.open_grocery()
        ingame_actions.open_filter_menu()

        while checks.check_all_switch() is True:
            ingame_actions.switch_all()
            time.sleep(1)

        while checks.check_cases_switch() is False:
            ingame_actions.switch_cases()
            time.sleep(1)

        ingame_actions.close_filter_menu()

        nomore_cases = False
        slot = 0
        x = FIRST_SLOT_INVENTORY_CORDS[0]
        cords = [x, FIRST_SLOT_INVENTORY_CORDS[1]]
        while not nomore_cases:
            if checks.check_if_case_is_apple(slot):
                slot += 1
                x += 100
                cords = [x, FIRST_SLOT_INVENTORY_CORDS[1]]
            if checks.check_if_case_is_book(slot):
                slot += 1
                cords = [x, FIRST_SLOT_INVENTORY_CORDS[1]]
            if checks.check_if_case_is_skip(slot):
                slot += 1
                x += 100
                cords = [x, FIRST_SLOT_INVENTORY_CORDS[1]]

            if checks.check_if_nomore_cases(slot):
                break
            print(f'Корды: {cords}')

            ingame_actions.toggle_autouse(cords[0], cords[1])
            time.sleep(1)
            ingame_actions.open_case(cords[0], cords[1])
            time.sleep(2)

            if checks.clock_menu_open():
                ingame_actions.choose_clock()
                ingame_actions.set_max_clock_menu()
                ingame_actions.agree_clock_choose()
                time.sleep(1)

            elif checks.red_recipe_open():
                ingame_actions.choose_red_accesory_receipt()
                ingame_actions.set_max_red_accesory_menu()
                ingame_actions.agree_red_receipt_choose()

        ingame_actions.close_inventory()
    except Exception as e:
        TGNotifier.send_break_msg('Ящики', '', e)


def run():
    windows.switch_windows(main)