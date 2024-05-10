from BuyerBot.main_funs.windows import Windows
from BuyerBot.main_funs.mouse_and_keboard import AHKActions
from BuyerBot.main_funs.images import Image

mouse_and_keyboard = AHKActions()
image = Image()
windows = Windows()


def get_server() -> dict:
    def _open_menu():
        mouse_and_keyboard.move(1775, 95, 0)
        mouse_and_keyboard.click()

    def _open_settings():
        mouse_and_keyboard.move(1690, 820, 0)
        mouse_and_keyboard.click()

    def _open_information():
        mouse_and_keyboard.move(1600, 180, 0)
        mouse_and_keyboard.click()

    while not image.menu_opened():
        _open_menu()

    while not image.settings_opened():
        _open_settings()

    while not image.information_opened():
        _open_information()

    server = image.get_server()
    hwnd = windows.get_hwnd_of_top_window()

    return {hwnd: server}


def get_all_servers():
    servers_and_hwnds_list = []
    for i in windows.get_all_l2m_windows():
        windows.open_window_by_hwnd(i)
        servers_and_hwnds_list.append(get_server())

    return servers_and_hwnds_list