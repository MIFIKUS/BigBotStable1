from BuyerBot.main_funs.mouse_and_keboard import AHKActions
from BuyerBot.main_funs.windows import Windows
from BuyerBot.main_funs.images import Image

import time


mouse_and_keyboard = AHKActions()
windows = Windows()
image = Image()


def main():
    def _open_menu():
        mouse_and_keyboard.move(1250, 70, 0)
        mouse_and_keyboard.click()

    def _open_market():
        mouse_and_keyboard.move(1500, 450, 0)
        mouse_and_keyboard.click()

    while not image.menu_opened():
        _open_menu()
        time.sleep(0.2)

    while not image.market_opened():
        _open_market()
        time.sleep(0.2)

    time.sleep(3)


def update_token():
    windows.switch_windows(main)
