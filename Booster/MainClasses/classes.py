from ahk import AHK
from PIL import Image as pil

import numpy as np
import pytesseract
import PIL.ImageGrab
import cv2

import win32gui
import win32com.client
import win32con
import win32process

import random
import time

import psutil

autohotkey = AHK()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def set_path():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                return path + '\\CollectionMaster'

PATH = set_path()

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
                time.sleep(0.1)
                autohotkey.click(direction='U')
                break
            except Exception:
                pass
        time.sleep(0.2)
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
            time.sleep(random.uniform(0.2, 0.4))
        self._kill_ahk_process()

    def _kill_ahk_process(self):
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'AutoHotkey.exe':
                    proc.kill()
        except Exception as e:
            print(e)
            print("AHK process doesn't exists anymore")

class Image:
    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):
        if need_for_taking_screenshot:
            if area_of_screenshot:
                PIL.ImageGrab.grab(bbox=area_of_screenshot).save(main_image_name)
            else:
                PIL.ImageGrab.grab().save(main_image_name)

        img_rgb = cv2.imread(main_image_name, 0)
        template = cv2.imread(template_image_name, 0)

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if func is None:
            for pt in zip(*loc[::-1]):
                print("Найдено совпадение")
                return True
            return False

        for pt in zip(*loc[::-1]):
            return list(pt)
        return False

    def delete_all_colors_except_one(self, file: str, colorMin_list: list, colorMax_list: list):
        """Функция для удаления всех цветов с картинки кроме одного"""
        im = cv2.imread(file)

        colorMin = np.array(colorMin_list, np.uint8)
        colorMax = np.array(colorMax_list, np.uint8)

        RGB  = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(RGB, colorMin, colorMax)

        inverse_cachement_mask = cv2.bitwise_not(mask)
        im[inverse_cachement_mask > 0] = [0, 0, 0]

        cv2.imwrite(file, mask)

    def take_screenshot(self, image_name, area_of_screenshot=None):
        if area_of_screenshot:
            PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
        else:
            PIL.ImageGrab.grab().save(image_name)

    def image_to_string(self, image_name, is_digits):
        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 6 -c tessedit_char_whitelist=0123456789.%(/)')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 3')
        return text

    def image_to_string_comma(self, image_name):
        text = pytesseract.image_to_string(image_name, config='--psm 6 -c tessedit_char_whitelist=0123456789,')
        return text

    def get_main_color(self, file):
        img = pil.open(file)
        colors = img.getcolors(512)  # put a higher value if there are many colors in your image
        max_occurence, most_present = 0, 0
        try:
            for c in colors:
                if (25, 30, 37) in c or (30, 35, 42) in c:
                    continue
                if c[0] > max_occurence:
                    (max_occurence, most_present) = c
            if type(most_present) is int:
                return (1, 1, 1)
            return most_present
        except TypeError:
            raise Exception("Too many colors in the image")

image = Image()
ahk = AHKActions()

class Windows:
    def switch_windows(self, func):
        shell = win32com.client.Dispatch("WScript.Shell")

        windows_list = self.__find_windows()

        print('Спиок открытых окок с линейкой', windows_list)

        if len(windows_list) > 0:
            for window in windows_list:
                for i in range(3):
                    shell.SendKeys('%')
                    win32gui.ShowWindow(window, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(window)
                    while self.is_screen_locked() is True:
                        self.unlock_screen()
                if self._is_dead() is True:
                    self._revive()
                    time.sleep(5)
                func()
                self.lock_screen()

    def _is_dead(self):
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\main_screen.jpg')
        if image.matching(f'{PATH}\\imgs\\screenshots\\main_screen.jpg', f'{PATH}\\imgs\\templates\\dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching(f'{PATH}\\imgs\\screenshots\\main_screen.jpg', f'{PATH}\\imgs\\templates\\dead2.png', need_for_taking_screenshot=True) is True:
            return True

    def _revive(self):
        def __send_to_last_location():
            ahk.move(x=350, y=180)
            ahk.click()

            ahk.move(x=250, y=350)
            ahk.click()

            ahk.move(x=420, y=460)
            ahk.click()

            time.sleep(4)

            ahk.move(x=1530, y=550)
            ahk.click()

        ahk.move(x=900, y=870)
        ahk.click()

        time.sleep(5)

        ahk.move(x=1250, y=80)
        ahk.click()
        image.take_screenshot('amount_of_free_revives.png', area_of_screenshot=(385, 600, 420, 640))
        try:
            amount_of_free_revives = int(pytesseract.image_to_string('amount_of_free_revives.png',
                                                                     config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
        except:
            ahk.move(x=1050, y=700)
            ahk.click()

            __send_to_last_location()
            return

        print(amount_of_free_revives)
        while image.matching('is_items_lose_via_death.png', 'adena.png', need_for_taking_screenshot=True, area_of_screenshot=(430, 600, 480, 650)) is False:
            ahk.move(x=500, y=620)
            ahk.click()

        if amount_of_free_revives == 0:
            ahk.esc()
            __send_to_last_location()
            return

        counter = 0
        if amount_of_free_revives > 3:
            amount_of_free_revives = 3
        else:
            amount_of_free_revives = 1

        for i in range(amount_of_free_revives):
            ahk.move(x=500, y=250+counter)
            ahk.click()
            counter += 100

        ahk.move(x=520, y=740)
        ahk.click()

        ahk.move(x=1050, y=700)
        ahk.click()

        ahk.move(x=400, y=190)
        ahk.click()

        while image.matching('is_items_lose_via_death.png', 'adena.png', need_for_taking_screenshot=True, area_of_screenshot=(430, 600, 480, 650)) is False:
            ahk.move(x=500, y=620)
            ahk.click()

        for i in range(4):
            ahk.move(x=500, y=250+(i*100))
            ahk.click()

        ahk.move(x=520, y=740)
        ahk.click()
        ahk.move(x=1050, y=700)
        ahk.click()

        ahk.move(x=530, y=170)
        ahk.click()


        __send_to_last_location()

    def is_screen_locked(self):
        for i in range(2):
            is_locked = image.matching(f'{PATH}\\imgs\\screenshots\\main_screen.jpg', f'{PATH}\\imgs\\templates\\screen_is_locked.png', need_for_taking_screenshot=True)
        return is_locked

    def unlock_screen(self):
        ahk.move(x=960, y=540)
        ahk.drag(x=100, y=100, relative=True)

    def lock_screen(self):
        ahk.move(x=73, y=633)
        ahk.click()
        time.sleep(1)
        ahk.move(x=960, y=540)
        ahk.click()

    def __find_windows(self, window_name='Lineage2M'):

        hwnd_list = []  # список для хранения hwnd найденных окон

        # функция для проверки, является ли окно верхним уровнем
        def __is_toplevel(hwnd):
            return win32gui.GetParent(hwnd) == 0 and win32gui.IsWindowVisible(hwnd)  # убедиться, что окно видимо

        # перечисление всех верхних уровней окон
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd) if __is_toplevel(hwnd) else None, hwnd_list)

        # фильтрация только окон с нужным именем
        lst_processes = [hwnd for hwnd in hwnd_list if window_name in win32gui.GetWindowText(hwnd)]

        if lst_processes:
            return lst_processes  # возвращает список hwnd, если окна найдены
        else:
            return None  # возвращает None, если окна не найдены

    def get_acc_name(self):
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd).replace('Lineage 2M |', '')