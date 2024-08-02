from Booster.Scrolls.functions import *
from Booster.Scrolls.ingame_actions import *

from Booster.MainClasses.classes import Windows

import time


windows = Windows()


def main():
    while not menu_opened():
        open_menu()
        time.sleep(1)

    open_craft_menu()
    time.sleep(1)

    choose_other()
    time.sleep(1)

    open_gods_orders()
    time.sleep(0.5)

    time.sleep(1)
    choose_order_signs()

    click_on_oder_sign()
    time.sleep(1)

    while craft_available():
        click_on_oder_sign()
        time.sleep(1)

        set_max_amount()
        craft()
        time.sleep(6)
        for _ in range(7):
            skip_craft()

    exit_from_craft_menu()


def run():
    windows.switch_windows(main)