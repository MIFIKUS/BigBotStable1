import time

from main_funs.mouse_and_keboard import AHKActions
from main_funs.images import Image
from ctypes import windll

import win32gui
import win32com.client
import win32con


ahk = AHKActions()
image = Image()

user32 = windll.user32
user32.SetProcessDPIAware()


class Windows:
    def switch_windows(self, func):
        shell = win32com.client.Dispatch("WScript.Shell")

        windows_list = self._find_windows('Lineage2M')

        print('Спиок открытых окок с линейкой', windows_list)

        if len(windows_list) > 0:
            for window in windows_list:
                for i in range(3):
                  shell.SendKeys('%')

                win32gui.ShowWindow(window, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(window)
                time.sleep(1)
                while self.is_screen_locked() is True:
                    self.unlock_screen()
                func()

    def unlock_screen(self):
        ahk.move(x=960, y=540)
        ahk.drag(100, 100, True)

    def is_screen_locked(self):
        is_locked = image.matching('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_screen_locked.png',
                                   'jwt_updater\\l2m_actions\\imgs\\templates\\screen_is_locked.png',
                                    need_for_taking_screenshot=True, threshold=0.8)
        return is_locked

    def open_window_by_hwnd(self, hwnd):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')

        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

    def open_fullscreen_window_by_hwnd(self, hwnd):
        def _is_fullscreen(hwnd):
            full_screen_rect = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
            try:
                rect = win32gui.GetWindowRect(hwnd)
                return rect == full_screen_rect
            except:
                return False

        if not _is_fullscreen(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def open_small_window_by_hwnd(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

    def _find_windows(self, window_name):
        def __is_toplevel(hwnd):
            return win32gui.GetParent(hwnd) == 0 and win32gui.IsWindowVisible(hwnd)

        hwnd_list = []

        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd) if __is_toplevel(hwnd) else None, hwnd_list)

        lst_processes = [hwnd for hwnd in hwnd_list if window_name in win32gui.GetWindowText(hwnd)]

        if lst_processes:
            return lst_processes
        else:
            return None

    def close_window_by_hwnd(self, hwnd):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def get_window_size_by_hwnd(self, hwnd) -> tuple:
        size = win32gui.GetWindowRect(hwnd)
        x = size[0]
        y = size[1]
        w = size[2] - x
        h = size[3] - y
        return w, h

    def open_instant_hand_history_menu(self):
        hwnd = self._find_windows('Instant Hand History')[0]
        self.open_window_by_hwnd(hwnd)

    def get_hwnd_by_name(self, name):
        return self._find_windows(name)[0]

    def get_hwnd_of_top_window(self):
        return win32gui.GetForegroundWindow()

    def get_all_l2m_windows(self):
        return self._find_windows('Lineage2M')
