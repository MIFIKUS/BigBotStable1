from ahk import AHK
import pyautogui
import psutil
import random
import time


autohotkey = AHK()


class AHKActions:
    def move(self, x, y, speed=3):
        while True:
            try:
                x += random.randint(0, 3)
                y += random.randint(0, 3)
                while autohotkey.mouse_position != (x, y):
                    autohotkey.mouse_move(x, y, speed=speed)
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def click(self):
        while True:
            try:
                autohotkey.click(direction='D')
                autohotkey.click(direction='U')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def drag(self, x, y, relative=True):
        while True:
            try:
                autohotkey.mouse_drag(x, y, relative=True)
                break
            except Exception:
                pass
        time.sleep(random.uniform(0.2, 0.3))
        self._kill_ahk_process()

    def press_down(self):
        while True:
            try:
                autohotkey.click(direction='D')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def press_up(self):
        while True:
            try:
                autohotkey.click(direction='D')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def wheel_down(self, amount_of_wheels=1):
        while True:
           try:
               for _ in range(amount_of_wheels):
                    autohotkey.wheel_down()
               break
           except Exception:
               pass
        self._kill_ahk_process()

    def wheel_up(self, amount_of_wheels=1):
        while True:
            try:
                for _ in range(amount_of_wheels):
                    autohotkey.wheel_up()
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def esc(self):
        while True:
            try:
                autohotkey.key_press('esc')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def end(self):
        while True:
            try:
                autohotkey.key_press('end')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def press_y(self):
        while True:
            try:
                autohotkey.key_press('y')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def press_i(self):
        while True:
            try:
                autohotkey.key_press('i')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def press_mouse(self):
        while True:
            try:
                autohotkey.click(direction='D')
                break
            except Exception:
                pass
        time.sleep(random.uniform(2, 3))
        while True:
            try:
                autohotkey.click(direction='U')
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def type(self, text):
        while True:
            try:
                autohotkey.type(text)
                break
            except Exception:
                pass
        self._kill_ahk_process()

    def ctrl_shift_c(self):
        for _ in range(2):
            pyautogui.hotkey('ctrl', 'shift', 'c')
            time.sleep(1)

    def _kill_ahk_process(self):
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'AutoHotkey.exe':
                    proc.kill()
        except Exception as e:
            print(e)
            print("AHK process doesn't exists anymore")
