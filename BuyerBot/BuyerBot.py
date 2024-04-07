from ahk import AHK
from PIL import Image as pil

import datetime
import json
import psutil

import PIL.ImageGrab
import numpy as np
import cv2
import pytesseract

import win32gui

import telebot

import time
import random

autohotkey = AHK()

class AHKActions:
    """Класс для взаимодействия с AHK"""
    def mouse_actions(self, action, x=0, y=0, text='', relative=False):
        """Фукнция для взаимодействия с AHK"""
        if action == 'move':
            while True:
                try:
                    if relative:
                        autohotkey.mouse_move(x, y, speed=0, relative=relative)
                    else:
                        while autohotkey.mouse_position != (x, y):
                            autohotkey.mouse_move(x, y, speed=3, relative=relative)
                    break
                except Exception:
                    pass
            time.sleep(random.uniform(0.2, 0.3))
            return

        elif action == 'click':
            while True:
                try:
                    autohotkey.click(direction='D')
                    time.sleep(0.15)
                    autohotkey.click(direction='U')
                    break
                except Exception:
                    pass

        elif action == 'drag':
            while True:
                try:
                    autohotkey.mouse_drag(x, y, relative=True)
                    break
                except Exception:
                    pass
            time.sleep(random.uniform(0.2, 0.3))
            return

        elif action == 'press down':
            while True:
                try:
                    autohotkey.click(direction='D')
                    break
                except Exception:
                    pass

        elif action == 'press up':
            while True:
                try:
                    autohotkey.click(direction='D')
                    break
                except Exception:
                    pass

        elif action == 'wheel':
            while True:
                try:
                    autohotkey.wheel_down()
                    break
                except Exception:
                    pass
            return

        elif action == 'wheel_up':
            while True:
                try:
                    autohotkey.wheel_up()
                    break
                except Exception:
                    pass
            return

        elif action == 'esc':
            try:
                autohotkey.key_press('esc')
            except Exception:
                pass
            return

        elif action == 'y':
            while True:
                try:
                    autohotkey.key_press('y')
                    break
                except Exception:
                    pass
            return

        elif action == 'i':
            while True:
                try:
                    autohotkey.key_press('i')
                    break
                except Exception:
                    pass
            return

        elif action == 'press':
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
            return

        elif action == 'type':
            while True:
                try:
                    autohotkey.type(text)
                    break
                except Exception:
                    pass
                time.sleep(random.uniform(0.2, 0.4))

        elif action == 'scroll':
            while True:
                try:
                    while autohotkey.mouse_position != (x, y):

                        autohotkey.click(direction='D')
                        autohotkey.mouse_move(x, y, speed=10)
                        autohotkey.click(direction='U')
                    break
                except Exception:
                    pass
        for proc in psutil.process_iter():
            if proc.name() == 'AutoHotkey.exe':
                proc.kill()

class Image:
    """Класс для взаимодействия с изображениями"""
    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):
        """Функция для сравнения двух изображений"""
        if need_for_taking_screenshot is True:
            if area_of_screenshot:
                PIL.ImageGrab.grab(bbox=area_of_screenshot).save(main_image_name)
            else:
                PIL.ImageGrab.grab().save(main_image_name)

        img_rgb = cv2.imread(main_image_name)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_image_name, 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if func is None:
            for pt in zip(*loc[::-1]):
                print("Найдено совпадение")
                return True
            return False
        i = 0
        for pt in zip(*loc[::-1]):
            return pt
        return False

    def take_screenshot(self, image_name, area_of_screenshot=None):
        """Функция для создания скришнотов"""
        if area_of_screenshot:
            if area_of_screenshot:
                PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
            else:
                PIL.ImageGrab.grab().save(image_name)

    def image_to_string(self, image_name, is_digits, fill_diamond=False):
        """Функция для перевода картинки в текст"""
        if fill_diamond is True:
            self.fill_the_diamond_with_black()

        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789/')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 6 --oem 3')
        return text

ahk = AHKActions()
image = Image()

class IngameActions:
    """Класс для внутриигровых взаимодействий"""
    def open_global_market(self):
        """Функция для открытия мирового аука"""
        ahk.mouse_actions('move', x=1780, y=90)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1700, y=350)
        ahk.mouse_actions('click')
        time.sleep(2)

        ahk.mouse_actions('move', x=1400, y=90)
        ahk.mouse_actions('click')
        time.sleep(2)

        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')

    def set_filter_for_red_items(self):
        """Функия для установления фильтра для красных шмоток"""
        ahk.mouse_actions('move', x=400, y=280)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1230, y=580)
        ahk.mouse_actions('click')
        self._confirm_filter()

    def set_filter_for_purple_items(self):
        """Функия для установления фильтра для фиолетовых шмоток"""
        ahk.mouse_actions('move', x=400, y=280)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=760, y=580)
        ahk.mouse_actions('click')
        self._confirm_filter()

    def _confirm_filter(self):
        """Функция для подтверждения фильтра"""
        ahk.mouse_actions('move', x=1000, y=960)
        ahk.mouse_actions('click')

    def scroll_market(self):
        """Функция для прокрутки аука"""
        while True:
            ahk.mouse_actions('move', x=1000, y=900)
            ahk.mouse_actions('scroll', x=1050, y=430)

class BuyerBot:
    """Основной класс бота где проходят всеUS\PycharmProjects\BigBot\venv\Scripts\python.exe "D:\Programs\PyCharm 2021.3\plugins\python\helpers\pydev\pydevconsole.py" --mode=client --port=57207
    необходимые расчеты и действия"""
    def __init__(self):
        self.MAXIMUM_PRICE_FOR_RED_ITEMS = 300
        self.MAXIMUM_PRICE_FOR_PURPLE_ITEMS = 1000

    def main(self):
        """Основной модуль бота"""
        ingame_actions = IngameActions()
        time.sleep(3)
        ingame_actions.scroll_market()
        pass

    def _detect_prices(self):
        """Функция для определния цены шмоток на ауке"""
        pass

    def _buy_item(self, is_book=False):
        """Функция для покупки шмоток"""
        pass

    def _confirm_price(self):
        """Функция для того чтобы удостовериться в том,
        что бот не ошибся в определении цены"""

    def _detect_soul_image(self):
        """Фукнция которая находит картинки душ, для того,
        чтобы бот понял, что аук кончился"""
        pass

    def _check_if_item_is_book(self):
        """Функция для проверки того, что шмотка является книгой,
        используется чтобы определить нужны ли дополнительные проверки
        цены и способа покупки"""
        pass

    def _check_what_sharpening_of_item_has_necessary_price(self):
        """Функция для опредления заточки шмотки с нужной ценой на ауке"""
        pass

    def _check_how_many_diamonds_on_account(self):
        """Функция для проверки того, сколько алмазов есть на аккаунте"""
        pass

buyer = BuyerBot()
def run():
    buyer.main()