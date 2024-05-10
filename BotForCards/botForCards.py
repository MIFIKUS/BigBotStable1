from ahk import AHK

import cv2
import numpy as np
import PIL.ImageGrab
import pytesseract

import win32gui
import win32com.client
import win32con

import TGNotifier

import time
import random
import psutil


MULTIPLIER = 1
PATH_TO_CARDS = r'C:\Users\MIFIKUS\PycharmProjects\BigBot\BotForCards\\'


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



autohotkey = AHK()

class Windows():
    def switch_windows(self, func):
        shell = win32com.client.Dispatch("WScript.Shell")

        windows_list = self.__find_windows()

        print('Спиок открытых окок с линейкой', windows_list)

        if len(windows_list) > 0:
            for window in windows_list:
                acc_name = win32gui.GetWindowText(window)
                print(acc_name)
                for i in range(3):
                    shell.SendKeys('%')

                win32gui.ShowWindow(window, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(window)
                for i in range(2):
                    if self.is_screen_locked() is True:
                        self.unlock_screen()
                if self._is_dead() is True:
                    self._revive()
                    time.sleep(5)
                func()

    def _is_dead(self):
        image.take_screenshot(f'{PATH_TO_CARDS}main_screen.jpg')
        if image.matching(f'{PATH_TO_CARDS}main_screen.jpg', f'{PATH_TO_CARDS}dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching(f'{PATH_TO_CARDS}main_screen.jpg', f'{PATH_TO_CARDS}dead2.png', need_for_taking_screenshot=True) is True:
            return True

    def _revive(self):
        def __send_to_last_location():
            ahk.mouse_actions('move', x=350, y=180)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=250, y=350)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=420, y=460)
            ahk.mouse_actions('click')

            time.sleep(4)

            ahk.mouse_actions('move', x=1530, y=550)
            ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=900, y=870)
        ahk.mouse_actions('click')

        time.sleep(5)

        ahk.mouse_actions('move', x=1250, y=80)
        ahk.mouse_actions('click')
        image.take_screenshot('amount_of_free_revives.png', area_of_screenshot=(385, 600, 420, 640))
        try:
            amount_of_free_revives = int(pytesseract.image_to_string('amount_of_free_revives.png',
                                                                     config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
        except:
            ahk.mouse_actions('move', x=1050, y=700)
            ahk.mouse_actions('click')

            __send_to_last_location()
            return

        print(amount_of_free_revives)

        if amount_of_free_revives == 0:
            ahk.mouse_actions('esc')
            __send_to_last_location()
            return

        counter = 0
        if amount_of_free_revives > 3:
            amount_of_free_revives = 3
        else:
            amount_of_free_revives = 1

        for i in range(amount_of_free_revives):
            ahk.mouse_actions('move', x=500, y=250+counter)
            ahk.mouse_actions('click')
            counter += 100

        ahk.mouse_actions('move', x=520, y=740)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1050, y=700)
        ahk.mouse_actions('click')

        counter = 0
        #if image.matching('is_items_lose_via_death.png', 'adena.png',need_for_taking_screenshot=True, area_of_screenshot=(325, 600, 420, 650)) is True:
        #    for i in range(4):
        #        ahk.mouse_actions('move', x=500, y=250+counter)
        #        ahk.mouse_actions('click')
        #        counter += 100
        #    ahk.mouse_actions('move', x=520, y=740)
        #    ahk.mouse_actions('click')
        #
        #    ahk.mouse_actions('move', x=1050, y=700)
        #    ahk.mouse_actions('click')


        ahk.mouse_actions('move', x=530, y=170)
        ahk.mouse_actions('click')


        __send_to_last_location()

    def is_screen_locked(self):
        for i in range(2):
            is_locked = image.matching(f'{PATH_TO_CARDS}main_screen.jpg', f'{PATH_TO_CARDS}screen_is_locked.png', need_for_taking_screenshot=True)
        return is_locked

    def unlock_screen(self):
        ahk.mouse_actions('move',x=960, y=540)
        ahk.mouse_actions('drag',x=100, y=100)

    def lock_screen(self):
        ahk.mouse_actions('move', x=73, y=633)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('move', x=960, y=540)
        ahk.mouse_actions('click')

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

class AHKActions():
    # Переменная action отвечает за то, какое действие нужно сделать. (кликнуть, перевести мышку, провести мышкой с нажатием)
    def mouse_actions(self, action, x=0, y=0, direction='R', text=''):
        if action == 'move':
            while True:
                try:
                    x += random.randint(0, 3)
                    y += random.randint(0, 3)
                    while autohotkey.mouse_position != (x, y):
                        autohotkey.mouse_move(x, y, speed=3)
                    break
                except:
                    pass

            time.sleep(random.uniform(0.2, 0.3))
            return
        elif action == 'click':
            while True:
                try:
                    autohotkey.click()
                    break
                except:
                    pass
            return

        elif action == 'drag':
            while True:
                try:
                    autohotkey.mouse_drag(x, y, relative=True)
                    break
                except:
                    pass
            time.sleep(random.uniform(0.2, 0.3))
            return
        elif action == 'press down':
            while True:
                try:
                    autohotkey.click(direction='D')
                    break
                except:
                    pass

        elif action == 'press up':
            while True:
                try:
                    autohotkey.click(direction='D')
                    break
                except:
                    pass
        elif action == 'wheel':
            while True:
                try:
                    autohotkey.wheel_down()
                    break
                except:
                    pass
            return

        elif action == 'esc':
            while True:
                try:
                    autohotkey.key_press('esc')
                    break
                except:
                    pass
            return
        elif action == 'y':
            while True:
                try:
                    autohotkey.key_press('y')
                    break
                except:
                    pass
            return

        elif action == 'i':
            while True:
                try:
                    autohotkey.key_press('i')
                    break
                except:
                    pass


            return

        elif action == 'press':
            while True:
                try:
                    autohotkey.click(direction='D')
                    break
                except:
                    pass
            time.sleep(random.uniform(2, 3))
            while True:
                try:
                    autohotkey.click(direction='U')
                    break
                except:
                    pass
            return
        elif action == 'type':
            while True:
                try:
                    autohotkey.type(text)
                    break
                except:
                    pass
                time.sleep(random.uniform(0.2, 0.4))
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'AutoHotkey.exe':
                    proc.kill()
        except Exception as e:
            print(e)
            print("AHK process doesn't exists anymore")

ahk = AHKActions()
class Image():

    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):

        if need_for_taking_screenshot is True:
            if area_of_screenshot:
                PIL.ImageGrab.grab(bbox=area_of_screenshot).save(main_image_name)
            else:
                PIL.ImageGrab.grab().save(main_image_name)

        img_rgb = cv2.imread(main_image_name)
        template = cv2.imread(template_image_name)

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if func is None:

            for pt in zip(*loc[::-1]):
                print("Найдено совпадение")
                return True
            return False
        i = 0
        for pt in zip(*loc[::-1]):
            i = pt
        try:
            return pt
        except:
            return False


    def take_screenshot(self, image_name, area_of_screenshot=None):
        if area_of_screenshot:
            if area_of_screenshot:
                PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
            else:
                PIL.ImageGrab.grab().save(image_name)

    def find_cards_in_inventory(self):
        time.sleep(1)
        self.take_screenshot(f'{PATH_TO_CARDS}inventory.png', area_of_screenshot=(1390, 230, 1800, 775))

        for i in range(1, 8):
            cords = self.matching(f'{PATH_TO_CARDS}inventory.png', f'{PATH_TO_CARDS}card_{i}.png', threshold=0.8, func=1)

            if cords:
                return cords
            else:
                print('Card ', i, 'not found')
        return False

ahk = AHKActions()
windows = Windows()
image = Image()

class InGame():
    def open_inventory(self):
        while image.matching(f'{PATH_TO_CARDS}is_inventory_opened.png', f'{PATH_TO_CARDS}inventory_opened.png',
                             need_for_taking_screenshot=True, threshold=0.7, area_of_screenshot=(1320, 165, 1410, 215)) is False:
            print('Инвентарь не открыт')
            autohotkey.key_press('i')
            time.sleep(1)

        ahk.mouse_actions('move', x=410, y=85)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1350, y=440)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')

        while image.matching(f'{PATH_TO_CARDS}is_filter_selected.png', f'{PATH_TO_CARDS}filter_is_selected.png',
                             need_for_taking_screenshot=True, area_of_screenshot=(1755, 255, 1810, 310), threshold=0.6) is True:
            ahk.mouse_actions('move', x=1600, y=280)
            ahk.mouse_actions('click')

        while image.matching(f'{PATH_TO_CARDS}is_filter_selected.png', f'{PATH_TO_CARDS}filter_is_selected.png',
                     need_for_taking_screenshot=True, area_of_screenshot=(1755, 335, 1810, 385), threshold=0.6) is False:
            ahk.mouse_actions('move', x=1600, y=350)
            ahk.mouse_actions('click')

        while image.matching(f'{PATH_TO_CARDS}is_filter_selected.png', f'{PATH_TO_CARDS}filter_is_selected.png',
                     need_for_taking_screenshot=True, area_of_screenshot=(1755, 490, 1810, 540), threshold=0.6) is False:
            ahk.mouse_actions('move', x=1600, y=520)
            ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1660, y=815)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1660, y=740)
        ahk.mouse_actions('click')

    def close_inventory(self):
        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1600, y=280)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')

    def open_card(self, cords):
        if cords is not False:
            x = cords[0] + 1400
            y = cords[1] + 300
            print(x,' ', y)
            ahk.mouse_actions('move', x=x, y=y)
            ahk.mouse_actions('click')
            ahk.mouse_actions('click')

            time.sleep(4)

            ahk.mouse_actions('move', x=930, y=950)
            ahk.mouse_actions('click')

            time.sleep(5)
            while image.matching(f'{PATH_TO_CARDS}card_menu.jpg', f'{PATH_TO_CARDS}go_to_result_button.png', need_for_taking_screenshot=True,
                                 threshold=0.65) is True:
                ahk.mouse_actions('move', x=850, y=950)
                ahk.mouse_actions('click')
                time.sleep(3)
            while image.matching(f'{PATH_TO_CARDS}card_menu.jpg', f'{PATH_TO_CARDS}repeat_button.png', need_for_taking_screenshot=True,
                                 threshold=0.7) is True:
                ahk.mouse_actions('move', x=850, y=950)
                ahk.mouse_actions('click')
                time.sleep(4)

                ahk.mouse_actions('move', x=930, y=950)
                ahk.mouse_actions('click')
                time.sleep(3)

            ahk.mouse_actions('esc')
            return True
        return False


windows = Windows()
image = Image()
ahk = AHKActions()
ingame = InGame()


def main():
    ingame.open_inventory()
    counter = 0
    while True:
        if ingame.open_card(image.find_cards_in_inventory()) is False:
            counter += 1
            if counter > 10:
                break
        else:
            counter = 0
    ingame.close_inventory()
    ahk.mouse_actions('esc')
    windows.lock_screen()

def run(multiplier, path):
    try:
        global MULTIPLIER
        global PATH_TO_CARDS

        MULTIPLIER = int(multiplier)
        PATH_TO_CARDS = f'{path}\BotForCards\\'
        windows.switch_windows(main)
    except Exception as e:
        TGNotifier.send_break_msg('Карточки', '', e)