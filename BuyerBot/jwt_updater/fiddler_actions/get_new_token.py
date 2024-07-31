from BuyerBot.main_funs.mouse_and_keboard import AHKActions
from BuyerBot.main_funs.windows import Windows
from tkinter import Tk

mouse_and_keyboard = AHKActions()
windows = Windows()


def get_token_from_headers(headers_raw):
    headers = {}
    lines = headers_raw.split('\n')
    for i in lines:
        if ': ' in i:
            i = i.split(': ')
            headers.update({i[0]: i[1]})

    return headers['Authorization']


def get_token() -> str:
    def _click_on_first_packet():
        mouse_and_keyboard.move(120, 100, 0)
        mouse_and_keyboard.click()

    def _go_to_last_packet():
        mouse_and_keyboard.end()

    def _copy_headers():
        mouse_and_keyboard.ctrl_shift_c()

    def _get_headers_from_clipboard():
        return Tk().clipboard_get()

    hwnd = windows.get_hwnd_by_name('Progress Telerik Fiddler Classic')
    windows.open_window_by_hwnd(hwnd)
    windows.open_small_window_by_hwnd(hwnd)
    windows.open_fullscreen_window_by_hwnd(hwnd)

    _click_on_first_packet()
    _go_to_last_packet()

    _copy_headers()
    headers_raw = _get_headers_from_clipboard()
    headers = get_token_from_headers(headers_raw)
    return headers
