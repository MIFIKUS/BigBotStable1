from BuyerBot.main_funs.mouse_and_keboard import AHKActions
from BuyerBot.main_funs.windows import Windows
from BuyerBot.main_funs.images import Image

import time
import psutil


mouse_and_keyboard = AHKActions()
windows = Windows()
image = Image()


def change_ip():
    def _close_chrome():
        for proc in psutil.process_iter(['pid', 'name']):
            if "Chrome".lower() in proc.info['name'].lower():
                p = psutil.Process(proc.info['pid'])
                p.terminate()

    def _disconnect():
        mouse_and_keyboard.move(1100, 600)
        mouse_and_keyboard.click()
        time.sleep(20)

    def _connect():
        for _ in range(2):
            mouse_and_keyboard.move(1100, 600)
            mouse_and_keyboard.click()
            time.sleep(20)

    hwnd = windows.get_hwnd_by_name('PlanetVPN')
    windows.open_window_by_hwnd(hwnd)

    _disconnect()
    windows.open_window_by_hwnd(hwnd)

    _connect()
    windows.open_window_by_hwnd(hwnd)

    _close_chrome()
