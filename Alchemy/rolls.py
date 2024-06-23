from ahk import AHK
from PIL import Image as pil
from difflib import SequenceMatcher
from os import listdir
from os.path import isfile, join
from threading import Thread

import psutil
import keyboard

import PIL.ImageGrab
import numpy as np
import cv2
import pytesseract

import win32gui

import telebot
import gspread
import mysql.connector
import TGNotifier

import time
import string
import random
import datetime
import json

#Время раз в которое удаляются значения из таблицы less_100_items
DIFERNCE_IN_TIME = 24

BOT_NAME = 'Алхимка'

ROLL_000_MINIMAL_PRICE_2ND_SLOT = 240
ROLL_000_MINIMAL_PRICE_2ND_SLOT_FOR_CHECK_1ST_SLOT = 130
ROLL_000_MINIMAL_PRICE_1ST_SLOT = 80
TOTAL_PRICE = 200

LIST_OF_BLUE_ITEMS_THAT_IN_2ND_SLOT = ('Магический Камень Духа Огня', 'Магический Камень Духа Воды', 'Магический Камень Духа Земли', 'Магический Камень Духа Тьмы', 'Цербер')

with open('settings.txt') as f:
    for i in f.readlines():
        if 'path' in i:
            path = i.split('=')[1]
            print(i)
        if 'Alchemy_minimal_price' in i:
            minimal_price = i.split('=')[1]
            print(minimal_price)

MINIMAL_PRICE_FOR_ROLL = int(minimal_price)

PATH_TO_ALCHEMY = path + '\\Alchemy\\'
LIST_OF_RARE_ITEMS = ''
LIST_OF_RARE_ITEMS_FOR_ALCHEMY = ''

ACESSORIES_LIST = ''
ROLL_00_ITEMS = ''
GAINED_ITEMS = []
LESS_100_ITEMS = []

items_on_market = None
accesory_items_on_market = None
out_of_blue_items = None
out_of_green_items = None
green_item_crafted = False


inventory_matrix = {}

red_slots = []
template_list_00 = []
with open(f'{PATH_TO_ALCHEMY}good_rare_items.txt', 'r', encoding='utf-8') as rare_items:
    LIST_OF_RARE_ITEMS = list(rare_items.read().split('\n'))

with open(f'{PATH_TO_ALCHEMY}good_rare_items.txt', 'r', encoding='utf-8') as rare_items:
    LIST_OF_RARE_ITEMS_FOR_ALCHEMY = list(rare_items.read().replace(' ', '').lower().split('\n'))

with open(f'{PATH_TO_ALCHEMY}good_rare_acessories.txt', 'r', encoding='utf-8') as accesories:
    ACESSORIES_LIST = accesories.read().replace(' ', '').split('\n')

with open(f'{PATH_TO_ALCHEMY}roll_888_bad_items_1st_slot.txt', 'r', encoding='utf-8') as first_slot_888_bad_items:
    ROLL_888_BAD_ITEMS_FIRST_SLOT = first_slot_888_bad_items.read().replace(' ', '').lower().split('\n')

with open(f'{PATH_TO_ALCHEMY}roll_888_bad_items_4th_slot.txt', 'r', encoding='utf-8') as fourth_slot_888_bad_items:
    ROLL_888_BAD_ITEMS_FOURTH_SLOT = fourth_slot_888_bad_items.read().replace(' ', '').lower().split('\n')

with open(f'{PATH_TO_ALCHEMY}servers_for_accounts.json', 'r', encoding='utf-8') as servers_for_accounts:
    SERVERS_FOR_ACCOUNTS = json.load(servers_for_accounts)

with open(f'{PATH_TO_ALCHEMY}roll_00_max_amount_on_server.json', 'r', encoding='utf-8') as max_amount:
    ROLL_00_MAX_AMOUNT_ON_SERVER = json.load(max_amount)

with open(f'{PATH_TO_ALCHEMY}roll_00_max_amount_on_server.json', 'r', encoding='utf-8') as max_amount:
    ROLL_00_MAX_AMOUNT_ON_SERVER = json.load(max_amount)

ADDITIONAL_GOOD_RARE_ITEMS_LIST = ('Исскуство Парных Мечей (Гнев Звука)',
                                   'Учебник Арблатетчика (Интеснивная Стрельба)',
                                   'Записи Жреца (Взрывная Стрела)',
                                   'Техника Двуручного Меча (Дикий Рев)',
                                   'Искусство Парных мечей (Двойное Оружие)',
                                   'Учебник Арбалетчика (Мастер Двойного Урона)',
                                   'Учебник Арбалетчика (Меткий Стрелок)',
                                   'Техника Двуручного Меча (Блокада)',
                                   'Манускрипт Демонического Меча (Цепная Звезда)',
                                   'Наставление по Древковому Оружию (Восстановление Гнева)',
                                   'Учебника Лучника (Замедляющий Выстрел)',
                                   'Манускрипт Демонического Меча (Обновление)',
                                   'Инструкнция к Магической Технике (Утонченный Разум)')

TG_USER_ID = 760238501
TG_API_KEY = '6030586977:AAEPBYOO-za3FoNCdkdVcDvQd63YoD_7PKk'
bot = telebot.TeleBot(TG_API_KEY)

MULTIPLIER = 1

autohotkey = AHK()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def decrease_roll_amount(acc_name):
    with open('alchemy_account_preset.txt', encoding='utf-8') as accs_presets:
        accs_presets = accs_presets.read().split('\n')

    print(accs_presets)

    new_list = []
    for i in accs_presets:
        if acc_name in i:
            amount = i.split(' ')[-2]
            print('amount ', amount)
            if int(amount) == 0:
                amount = 0
            info = i.replace(str(amount), str(int(amount)-1))
        else:
            info = i
        new_list.append(info)
    print(new_list)
    redacted_info = '\n'.join(new_list)

    print(redacted_info)

    with open('alchemy_account_preset.txt', 'w', encoding='utf-8', ) as accs_presets:
        accs_presets.write(redacted_info)

class AHKActions:
    # Переменная action отвечает за то, какое действие нужно сделать. (кликнуть, перевести мышку, провести мышкой с нажатием)
    def mouse_actions(self, action, x=0, y=0, text='', relative=False):

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
                    time.sleep(0.01)
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

        elif action == 'ctrl_a_backspace':
            while True:
                try:
                    for i in range(20):
                        autohotkey.key_press('Backspace')
                        break
                except Exception as e:
                    print(e)
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

        if area_of_screenshot:
            if area_of_screenshot:
                PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
            else:
                PIL.ImageGrab.grab().save(image_name)

    def image_to_string(self, image_name, is_digits, fill_diamond=False):

        if fill_diamond is True:
            self.fill_the_diamond_with_black()

        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789/')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 6 --oem 3')
        return text

    def _denoise_image(self, image_name):

        img = cv2.imread(image_name)
        img_bw = 255 * (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > 5).astype('uint8')

        se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

        mask = np.dstack([mask, mask, mask]) / 255
        out = img * mask
        cv2.imwrite(image_name, out)

    def is_inventory_overflow(self):
        if self.matching(f'{PATH_TO_ALCHEMY}is_inventory_overflow.jpg', f'{PATH_TO_ALCHEMY}inventory_is_overlow.png',
                         need_for_taking_screenshot=True, threshold=0.65) is True:

            print("Инвентарь переполнен. Замечен 1ым способом")
            return True
        if self.matching(f'{PATH_TO_ALCHEMY}is_inventory_overflow.jpg', f'{PATH_TO_ALCHEMY}inventory_is_overlow_2.png',
                         need_for_taking_screenshot=True, threshold=0.60) is True:

            print("Инвентарь переполнен. Замечен 2ым способом")
            return True

        return False

    def fill_the_diamond_with_black(self, file='minimal_price.png'):
        #смотрим минимальную цену, чтобы потом закрасить там кристалик
        img_rgb = cv2.imread(f'{PATH_TO_ALCHEMY}\\imgs\\{file}')

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(f'{PATH_TO_ALCHEMY}\\imgs\\diamond.png', 0)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (15, 18, 22), -1)

        cv2.imwrite(f'{PATH_TO_ALCHEMY}{file}', img_rgb)


    def get_main_color(self, file, colors_amount=1024):
        img = pil.open(file)
        colors = img.getcolors(colors_amount)  # put a higher value if there are many colors in your image
        colors = sorted(colors)
        if (0,0,0) in colors:
           colors.remove(colors[0])
        return colors[0][1]

    def optimise_forecast_letter_image(self, file):
        im = cv2.imread(file)

        # Define lower and upper limits of our blue
        BlueMin = np.array([0,  0, 0], np.uint8)
        BlueMax = np.array([230, 230, 230], np.uint8)

        # Go to HSV colourspace and get mask of blue pixels
        HSV  = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(HSV, BlueMin, BlueMax)

        # Make all pixels in mask white
        im[mask>0] = [0, 0, 0]
        cv2.imwrite(file, im)

        foresast_letter = self.image_to_string(file, is_digits=False)
        return foresast_letter

    def delete_all_colors_except_blue(self, file):
        im = cv2.imread(file)
        BlueMin = np.array([10, 110, 190], np.uint8)
        BlueMax = np.array([35, 150, 225], np.uint8)

        # Go to HSV colourspace and get mask of blue pixels
        HSV = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(HSV, BlueMin, BlueMax)

        inverse_cachement_mask = cv2.bitwise_not(mask)
        # Make all pixels in mask white
        im[inverse_cachement_mask>0] = [0, 0, 0]
        cv2.imwrite('blue.png', im)

    def delete_all_colors_except_green(self, file):
        im = cv2.imread(file)

        GreenMin = np.array([15, 150, 70], np.uint8)
        GreenMax = np.array([30, 175, 90], np.uint8)

        # Go to HSV colourspace and get mask of blue pixels
        HSV  = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(HSV, GreenMin, GreenMax)
        #inverse_catchment_mask = (np.logical_not(np.where(np.isnan(mask), 1, np.nan)))
        inverse_cachement_mask = cv2.bitwise_not(mask)
        # Make all pixels in mask white
        im[inverse_cachement_mask>0] = [0, 0, 0]
        cv2.imwrite('green.png', im)

    def delete_all_colors_except_red(self, file):
        im = cv2.imread(file)

        GreenMin = np.array([160, 30, 60], np.uint8)
        GreenMax = np.array([255, 45, 75], np.uint8)

        # Go to HSV colourspace and get mask of blue pixels
        HSV  = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(HSV, GreenMin, GreenMax)

        inverse_cachement_mask = cv2.bitwise_not(mask)
        # Make all pixels in mask white
        im[inverse_cachement_mask>0] = [0, 0, 0]
        cv2.imwrite('red.png', im)

    def is_forecast_opened(self):
        start_time = time.time()
        self.take_screenshot(f'{PATH_TO_ALCHEMY}imgs\\is_forecast_opened.png', area_of_screenshot=(1040, 790, 1050, 800))
        color = self.get_main_color(f'{PATH_TO_ALCHEMY}imgs\\is_forecast_opened.png')
        print(color)
        end_time = time.time()
        print(end_time-start_time)
        if (200 < color[0] < 220) and (85 < color[1] < 105) and (0 < color[2] < 15):
            return True
        print('Предсказание не открыто, пробует еще раз')
        return False

    def black_and_white_80_888(self, file, roll):

        if roll == '80' or roll == '888':
            ColorMin = [110, 20, 45]
            ColorMax = [255, 70, 100]
        elif roll == '66':
            ColorMin = [15, 120, 200]
            ColorMax = [30, 138, 220]
        else:
            raise Exception(f'black_and_white_80_888 вызывается не там где нужно! Roll: {roll}')

        im = cv2.imread(file)

        GreenMin = np.array(ColorMin, np.uint8)
        GreenMax = np.array(ColorMax, np.uint8)

        # Go to HSV colourspace and get mask of blue pixels
        HSV  = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(HSV, GreenMin, GreenMax)

        inverse_cachement_mask = cv2.bitwise_not(mask)
        # Make all pixels in mask white
        im[inverse_cachement_mask>0] = [0, 0, 0]
        im[mask>0] = [255, 255, 255]
        cv2.imwrite(file, im)

    def is_5th_slot_in_alchemy_not_empty(self):
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_5th_slot_not_empty.png', area_of_screenshot=(1100, 700, 1210, 820))
        is_slot_empty = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_5th_slot_not_empty.png',
                                           f'{PATH_TO_ALCHEMY}\\imgs\\empty_slot_in_alchemy.png',
                                           need_for_taking_screenshot=False)
        if is_slot_empty is True:
            return False
        return True

    def check_if_there_is_error_after_unlock_window(self):
        self.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_there_error_button.png', area_of_screenshot=(550, 420, 1250, 800))
        is_there_error = self.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_there_error_button.png',
                                       f'{PATH_TO_ALCHEMY}\\imgs\\error_after_unlock_button.png',
                                       need_for_taking_screenshot=False, threshold=0.7)

        if is_there_error:
            ahk.mouse_actions('move', x=950, y=620)
            ahk.mouse_actions('click')
            time.sleep(3)

    def is_dead(self):
        """Проверка на то, умер ли персонаж"""

        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_dead.png', area_of_screenshot=(730, 825, 1125, 920))

        dead_button_1 = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_dead.png',
                                       f'{PATH_TO_ALCHEMY}\\imgs\\dead.png', need_for_taking_screenshot=False)

        dead_button_2 = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_dead.png',
                                       f'{PATH_TO_ALCHEMY}\\imgs\\dead2.png', need_for_taking_screenshot=False)

        if dead_button_1 or dead_button_2:
            time.sleep(10)
            self._revive()
            return True
        return False

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
        while image.matching('is_items_lose_via_death.png', 'adena.png', need_for_taking_screenshot=True, area_of_screenshot=(430, 600, 480, 650)) is False:
            ahk.mouse_actions('move', x=500, y=620)
            ahk.mouse_actions('click')

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

        ahk.mouse_actions('move', x=400, y=190)
        ahk.mouse_actions('click')

        while image.matching('is_items_lose_via_death.png', 'adena.png', need_for_taking_screenshot=True, area_of_screenshot=(430, 600, 480, 650)) is False:
            ahk.mouse_actions('move', x=500, y=620)
            ahk.mouse_actions('click')

        for i in range(4):
            ahk.mouse_actions('move', x=500, y=250+(i*100))
            ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=520, y=740)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1050, y=700)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=530, y=170)
        ahk.mouse_actions('click')

        __send_to_last_location()

    def check_4th_slot_empty(self):
        """Проверка на то, пустой ли 4ый слот в химке"""
        self.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_4th_slot_empty.png', area_of_screenshot=(1000, 785, 1110, 900))

        slot_empty = self.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_4th_slot_empty.png', f'{PATH_TO_ALCHEMY}\\imgs\\empty_4th_slot.png',
                                   need_for_taking_screenshot=False, threshold=0.7)

        return slot_empty

    def get_gained_item_slot(self) -> tuple or bool:
        y_additional = 0
        for column in range(6):
            x_additional = 0
            for row in range(4):
                self.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_gained.png', (1407+x_additional, 330+y_additional,
                                                                                                                  1510+x_additional, 431+y_additional))

                if self.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_gained.png', f'{PATH_TO_ALCHEMY}\\imgs\\red_dot.png',
                                 threshold=0.7):
                    return column, row

                x_additional += 100
            y_additional += 100

        return False

    def get_minimal_price(self) -> int or bool:
        self.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\minimal_price.png', area_of_screenshot=(1220, 459, 1360, 495))
        minimal_price = self.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\minimal_price.png', True, True)

        try:
            return minimal_price
        except Exception as e:
            print(f'Невозможно получить минимальную цену Ошибка {e}')
            return False

    def clear_number_for_detect_seted_price(self, file):
        im = cv2.imread(file)

        BlueMin = np.array([180, 70, 0], np.uint8)
        BlueMax = np.array([255, 110, 10], np.uint8)

        # Go to HSV colourspace and get mask of blue pixels
        HSV  = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(HSV, BlueMin, BlueMax)

        inverse_cachement_mask = cv2.bitwise_not(mask)
        # Make all pixels in mask white
        im[inverse_cachement_mask>0] = [0, 0, 0]
        cv2.imwrite(file, mask)

    def get_amount_of_slots(self):
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\slots.png', area_of_screenshot=(150, 930, 235, 980))
        return int(image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\slots.png', is_digits=True).replace('\n', '').split('/')[0])


ahk = AHKActions()
image = Image()


class Telegram:
    def __init__(self, hwnd):
        self.hwnd = hwnd

    def send_msg_in_tg(self, type=''):
        acc_name = win32gui.GetWindowText(self.hwnd)
        acc_name = acc_name.replace('Lineage2M l ', '')

        if type == 'overflow':
            bot.send_message(TG_USER_ID, f'На аккаунте {acc_name} переполнен инвентарь (')
            print("Сообщение в тг отправлено")

        if type == 'not_found_items':
            bot.send_message(TG_USER_ID, f'На аккаунте {acc_name} не достаточно шмоток для ролла')


class GoogleSheets:
    def __init__(self):
        self.SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1lICdsTXnU4COlW1Bwj7A3rTOVFyBHs9UX__uiXmaDGE/edit#gid=0'
        self.letter_and_cells = {
            'Вы чувствуете энергию чистой магии': '3',
            'Вы чувствуете энергию кружащуюся в воздухе энергию древней магии': '6',
            'Вы чувствуете вибрацию энергии мощной магии': '9',
            'Круг перевоплощения сияет ослепляющим светом': '14',
            'Круг перевоплощения мерцает': '17',
            'Круг перевоплощения ярко сияет': '20',
            'Ослепительная золотая аура заполняет круг перевоплощения' : '25',
            'Таинственная аура окружает круг перевоплощения': '28',
            'Священная аура наполняет круг перевоплощения': '31'
        }

    def write_google(self, letter, slot):
        cell = self._get_cell_for_letter_and_slot(letter, slot)
        if cell is False:
            print('Не смог определить название круга')
            return

        try:
            gs = gspread.service_account('credential_for_statistics.json')
            sh = gs.open_by_url(self.SPREADSHEET_URL)
            value_in_cell = int(sh.sheet1.get(cell)[0][0]) + 1

            sh.sheet1.update(cell, value_in_cell)
            return True
        except Exception as e:
            print(f'[ERROR] Place: write_google, {e}')
            return False

    def _get_cell_for_letter_and_slot(self, letter, slot):
        print('letter is ', letter)
        letter = letter.replace(' ', '').replace('\n', '').lower()
        for i in self.letter_and_cells.items():
            letter_in_dict = i[0].replace(' ', '').lower()
            cell_in_dict = i[1]
            print(letter)
            if SequenceMatcher(a=letter_in_dict, b=letter).ratio() > 0.8:
                cell_in_dict = list(string.ascii_uppercase)[slot+1] + cell_in_dict
                return cell_in_dict
        return False

    def write_amount_of_gained_items_in_table(self, list_of_servers_and_slots):
        try:
            url = "https://docs.google.com/spreadsheets/d/1qwPa93plt7a_ArFfi05tQZ3pl5o1BSfcIet9GtePkFo/edit#gid=0"
            gs = gspread.service_account('credential_for_statistics.json')
            sh = gs.open_by_url(url)

        except Exception as e:
            print(f'[ERROR] Place: write_amount_of_gained_items_in_table, {e}')
            return False

        list_of_data_to_write = []

        for i in list_of_servers_and_slots:
            list_of_data_to_write.append([f'{i[1]}/192'])

        start_time = time.time()
        sh.sheet1.update('K4:K27', list_of_data_to_write)
        print('Запись в таблицу заняла', time.time() - start_time)
        return True

#    def reconnect(self, func):
#        def wrapper():
#            AMOUNT_OF_TRIES = 3
#            for _ in range(AMOUNT_OF_TRIES):
#                res = func()
#                if res is True:
#                    print('Удалось подключиться')
#                    return
#                print('Не удалось переподключиться. Пробуем еще раз')
#            raise Exception(f'Не удалось подключиться за {AMOUNT_OF_TRIES} раз. Выход из программы.')
#
#        return wrapper

class DataBase:
    def __init__(self):
        #self.host = '192.168.0.10'
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'BigBot'
        #self.password = 'root'
        self.AMOUNT_OF_ROLL_00_ITEMS = 188

    def add_to_gained_items(self, acc_name, item_name):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            server_name = SERVERS_FOR_ACCOUNTS.get(acc_name)
            item_name = item_name.replace(' ', '').replace('\n', '').lower()
            query = f'''
                INSERT INTO alchemy.gained_items(item_name, server_name)
                VALUES ("{item_name}" , "{server_name}")
            '''
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print("Ошибка ", e, "\n",
                  "Аккаунт ", 'ao_gained_items SQL')

    def add_to_less_100_items(self, acc_name, item_name):
        print('Начало функции записи в таблицу шмоток стоимостью меньше:', MINIMAL_PRICE_FOR_ROLL)

        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            print('Аккаунт:', acc_name)

            server_name = SERVERS_FOR_ACCOUNTS.get(acc_name)
            print('Сервер:', server_name)

            query = f'''
                    INSERT INTO alchemy.less_100_items(item_name, server_name, date)
                    VALUES ("{item_name}" , "{server_name}", "{datetime.datetime.now()}")
                '''
            print('SQL запрос: ', query)
            cursor.execute(query)
            cursor.close()
            print('SQL запрос успешно выполнен!')
        except Exception as e:
            print("Ошибка ", e, "\n",
                  "Аккаунт ", acc_name, "\n",
                  'Место add_to_less_100_items SQL')

    def get_values_from_gained_items(self, acc_name):
        global GAINED_ITEMS
        GAINED_ITEMS = []
        try:
            server_name = SERVERS_FOR_ACCOUNTS.get(acc_name)

            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
            connection.autocommit = True
            cursor = connection.cursor()
            query = f'''
                    SELECT * FROM alchemy.gained_items WHERE server_name = "{server_name}"
                '''
            cursor.execute(query)

            result = cursor.fetchall()

            for i in result:
                GAINED_ITEMS.append(i[0])
            cursor.close()
        except Exception as e:
            print("Ошибка ", e, "\n",
                  "Аккаунт ", acc_name, "\n",
                  'Место get_values_from_gained_items SQL')

    def get_values_from_less_100_items(self, acc_name):
        global LESS_100_ITEMS
        LESS_100_ITEMS = []
        try:
            server_name = SERVERS_FOR_ACCOUNTS.get(acc_name)

            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
            connection.autocommit = True
            cursor = connection.cursor()
            query = f'''
                    SELECT * FROM alchemy.less_100_items WHERE server_name = "{server_name}"
                '''
            cursor.execute(query)

            result = cursor.fetchall()

            for i in result:
                LESS_100_ITEMS.append(i[0])
            cursor.close()

        except Exception as e:
            print("Ошибка ", e, "\n",
              "Аккаунт ", acc_name, "\n",
              'Место get_values_from_less_100_items SQL')

    def update_less_100_items(self, acc_name):
        global LESS_100_ITEMS
        LESS_100_ITEMS = []
        try:
            server_name = SERVERS_FOR_ACCOUNTS.get(acc_name)

            print(f'Account: {acc_name} Server: {server_name}')

            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
            connection.autocommit = True
            cursor = connection.cursor()

            query = f'''
                    SELECT * FROM alchemy.less_100_items
                '''

            print('Select query is', query)

            cursor.execute(query)

            result = cursor.fetchall()

            for i in result:
                differnce = abs((i[2] - datetime.datetime.now()).total_seconds()) / (60 * 60)
                print('Для шмотки', i[0], 'разница во времени', differnce)
                if differnce >= DIFERNCE_IN_TIME:
                    query = f'''
                    DELETE FROM alchemy.less_100_items WHERE item_name="{i[0]}" AND server_name = "{server_name}"
                    '''

                    print('Delete query is', query)

                    cursor.execute(query)

                    print('Разница во времени больше', DIFERNCE_IN_TIME, 'ч')
                    print('Шмотка:', i[0], 'удалена из треш слотов')

            cursor.close()
        except Exception as e:
            print("Ошибка ", e, "\n",
                  "Аккаунт ", acc_name, "\n",
                  'Место update_less_100_items SQL')

    def get_amount_of_item_in_db(self, item_name, acc_name):
        try:
            server_name = SERVERS_FOR_ACCOUNTS.get(acc_name)

            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
            connection.autocommit = True
            cursor = connection.cursor()
            query = f'''
                    SELECT * FROM alchemy.gained_items WHERE item_name = "{item_name}" AND server_name = "{server_name}"
                '''
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return len(result)

        except Exception as e:
            print("Ошибка ", e, "\n",
                  "Аккаунт ", acc_name, "\n",
                  'Место get_amount_of_item_in_db SQL')

    def update_gained_items_google_table(self):
        start = time.time()
        with open(f'{PATH_TO_ALCHEMY}\\rol_00_items.txt', 'r', encoding='utf-8') as items:
            rolL_00_items_list = items.read().replace(' ', '').lower().split('\n')

        list_of_servers_and_gained_slots = []

        LIST_OF_SERVERS = ('Б1', 'Б2', 'Б3', 'Б4', 'Б5', 'Б6', 'З1', 'З2',
                           'З3', 'З4', 'З5', 'З6', 'Л1', 'Л2', 'Л3', 'Л4',
                           'Л5', 'Л6', 'Э1', 'Э2', 'Э3', 'Э4', 'Э5', 'Э6', )
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        connection.autocommit = True
        cursor = connection.cursor()
        for i in LIST_OF_SERVERS:
            query = f'SELECT * FROM alchemy.gained_items WHERE server_name = "{i}"'
            cursor.execute(query)
            list_of_gained_items_and_servers = cursor.fetchall()
            amount_of_items_in_db = 0
            for a in list_of_gained_items_and_servers:
                if a[0] in rolL_00_items_list:
                    amount_of_items_in_db += 1
            list_of_servers_and_gained_slots.append((i, amount_of_items_in_db))
            print('Данные в таблицу по серверу', i, 'добавлены')
        cursor.close()

        google.write_amount_of_gained_items_in_table(list_of_servers_and_gained_slots)

        print('Данные в таблице выпавших шмоток обновлены')
        print('Весь процесс записи выпавших шмоток занял', time.time()-start)



def sort_inventory():
    ahk.mouse_actions('i')
    time.sleep(0.2)

    ahk.mouse_actions('move', x=1660, y=820)
    ahk.mouse_actions('click')

    ahk.mouse_actions('move', x=1660, y=520)
    ahk.mouse_actions('click')

    ahk.mouse_actions('esc')

    time.sleep(1)

def get_acc_name():
    with open(f"{PATH_TO_ALCHEMY}acounts_cells_for_sheet.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
        acounts_cells_for_sheet = data

    def __go_to_server_settings():
        ahk.mouse_actions('move', x=1780, y=75)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1690, y=820)
        ahk.mouse_actions('click')

        time.sleep(4)

        ahk.mouse_actions('move', x=1600, y=180)
        ahk.mouse_actions('click')

    for i in range(5):
        image.take_screenshot(f"{PATH_TO_ALCHEMY}\\imgs\\acc_name.png", area_of_screenshot=(150, 0, 300, 40))
        acc_name_image = cv2.imread(f"{PATH_TO_ALCHEMY}\\imgs\\acc_name.png")

        gray = cv2.cvtColor(acc_name_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        invert = 255 - thresh

        acc_name = pytesseract.image_to_string(invert, lang='rus+eng', config='--psm 6').replace('\n\n', ' ').replace('\n', ' ')
        acc_name = ''.join([i for i in acc_name if i != ' ']).replace('.', '').replace(',', '').replace('`', '').replace("'",
                                                                                                                         '')
        print(acc_name)
        if len(acc_name) > 2:
            if acc_name in acounts_cells_for_sheet.keys():
                print('Удалось получить название аккаунта по верхней левой надписи')
                print(acc_name)
                return acc_name
            else:
                print('Не удалось получить название аккаунта по верхней левой надписи пробует еще раз')
                time.sleep(0.2)
            print('Не удалось получить название аккаунта по верхней левой надписи пробует еще раз')

    print('Не удалось получить название аккаунта. Переход к следующему способу')

    __go_to_server_settings()

    for i in range(5):
        image.take_screenshot(f"{PATH_TO_ALCHEMY}\\imgs\\acc_name.png", area_of_screenshot=(1200, 265, 1445, 315))
        acc_name_image = cv2.imread(f"{PATH_TO_ALCHEMY}\\imgs\\acc_name.png")

        gray = cv2.cvtColor(acc_name_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        invert = 255 - thresh

        acc_name = pytesseract.image_to_string(invert, lang='rus+eng', config='--psm 6').replace('\n\n', ' ').replace('\n', ' ')
        acc_name = ''.join([i for i in acc_name if i != ' ']).replace('.', '').replace(',', '').replace('`', '').replace("'",
                                                                                                                         '')
        print(acc_name)

        if acc_name in acounts_cells_for_sheet.keys():
            print('Удалось получить название аккаунта по названию в настройках')
            print(acc_name)
            ahk.mouse_actions('esc')
            return acc_name
        else:
            print('Не удалось получить название аккаунта по названию в настройках пробует еще раз')
            time.sleep(0.2)
    ahk.mouse_actions('esc')
    print('Не удалось получить название аккаунта. Боль, депрессия и разочарование(((')

google = GoogleSheets()
sql = DataBase()

adena_wasted = 0
diamonds_wasted = 0
items_bought = {}
class Rolls():
    def __init__(self):
        self.RED = 'red'
        self.GREEN = 'green'
        self.BLUE = 'blue'
        self.GOLD = 'gold'
        self.WHITE = 'white'
        self.PLUS_0_ACCESORY = '+0'
        self.PLUS_1_ACCESORY = '+1'
        self.PLUS_2_ACCESORY = '+2'
        self.PLUS_3_ACCESORY = '+3'
        self.PLUS_0_RED_ACCESORY = 'red+0'
        self.PLUS_1_RED_ACCESORY = 'red+1'
        self.PLUS_2_RED_ACCESORY = 'red+2'
        self.PLUS_3_RED_ACCESORY = 'red+3'
        self.PLUS_4_RED_ACCESORY = 'red+4'
        self.PLUS_5_RED_ACCESORY = 'red+5'
        self.SHARP_RED = 'red+'
        self.PIECE = 'piece'
        self.PIECE_NOT_PLUS_8 = 'piece_not_8'

    def make_roll(self, forecast_colors, item_list_and_colors, need_except_accesories, need_except_sharp,
                  slots, totaling_prices, list_of_appropriate_roll_items, red_check, need_for_check_roll_items_name, items_list,
                  roll_amount, tg, hwnd, need_check_sql, is_888=False, is_80=False, need_sequence_matching=False, accesory_items_list=None,
                  need_find_by_image=False, roll=None, need_to_roll=True, need_check_symbol=False):
        try:
            global adena_wasted
            global diamonds_wasted
            global items_bought
            global template_list_00

            image.check_if_there_is_error_after_unlock_window()

            sql.update_gained_items_google_table()
            start_time = time.time()
            template_list_00 = []
            adena_wasted = 0
            diamonds_wasted = 0
            items_bought = {}
            acc_name = win32gui.GetWindowText(hwnd)
            acc_name = acc_name.replace('Lineage2M l ', '')
            if 'Lineage2M' in acc_name:
                print('Не удалось получить название аккаунта по названию окна, переход к следующему способу')
                acc_name = get_acc_name()

            if need_check_sql:
                sql.update_less_100_items(acc_name)
                sql.get_values_from_gained_items(acc_name)
                sql.get_values_from_less_100_items(acc_name)

            if roll == '40' or roll == '50' or roll == '50_plus':
                while True:
                    keyboard.add_hotkey('ctrl+f12', lambda: self._make_roll_for_40_50_roll(forecast_colors=forecast_colors, roll=roll, need_check_symbol=need_check_symbol,
                                                                                           need_find_by_image=need_find_by_image, list_of_appropriate_roll_items=list_of_appropriate_roll_items,
                                                                                           slots=slots))
                    keyboard.wait()

            ahk.mouse_actions('move', x=100, y=100)
            self._go_to_alchemy()
            time.sleep(1)
            self._reset_roll()
            is_roll_done = False

            is_choose_items_done = False

            while is_choose_items_done is False:
                is_choose_items_done = self.choose_necceary_items_from_inventory(item_list_and_colors,
                                                                                 need_except_accesories,
                                                                                 need_except_sharp,
                                                                                 need_for_check_roll_items_name,
                                                                                 items_list,
                                                                                 accesory_items_list,
                                                                                 tg, roll)
                if is_choose_items_done == "GREEN ERROR":
                    return None, None, 0, 0, 0, {}, 0, "Не нашел зеленую шмотку, скип", 0
            while is_roll_done is False:

                is_color_good = False

                while not is_color_good:
                    if image.is_dead():
                        self._go_to_alchemy()
                        time.sleep(2)
                    self._repeat_forecast()
                    adena_wasted += 10000
                    time.sleep(0.6)
                    color_true, color_of_forecast = self.check_neccesary_color_of_forecast(forecast_colors)
                    if color_true is True:
                        forecast_not_opened_counter = 0
                        while not image.is_forecast_opened():
                            forecast_not_opened_counter += 1
                            self._open_forecast()
                            if forecast_not_opened_counter >= 1000:
                                if image.is_dead():
                                    self._go_to_alchemy()
                                self._go_to_alchemy()
                                forecast_not_opened_counter = 0
                        if self.is_diamonds_in_forecast():
                            ahk.mouse_actions('esc')
                        else:
                            print('Ролл без кристалов на нужном свечении создан')
                            is_color_good = True
                    else:
                        continue

                if self.check_items_price(slots, list_of_appropriate_roll_items, red_check,
                                          need_for_totaling_prices=totaling_prices, need_check_sql=need_check_sql, hwnd=hwnd,
                                          color_of_forecast=color_of_forecast, is_888=is_888, is_80=is_80,
                                          need_sequence_matching=need_sequence_matching, need_find_by_image=need_find_by_image,
                                          roll=roll, need_check_symbol=need_check_symbol) is False:
                    ahk.mouse_actions('esc')
                    continue
                else:
                    time.sleep(0.2)
                    ahk.mouse_actions('esc')
                    if need_to_roll is False:
                        raise Exception('Ролл найден')

                    time.sleep(0.5)
                    image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\letter_in_forecast.png', area_of_screenshot=(525, 675, 1345, 715))

                    forecast_letter = image.optimise_forecast_letter_image(f'{PATH_TO_ALCHEMY}\\imgs\\letter_in_forecast.png')

                    self._start_roll()
                    adena_wasted += 20000
                    time.sleep(6)

                    gained_item, slot = self._get_slot_and_name_of_item_that_gained()

                    print('gained_item', gained_item)
                    print('slot', slot)

                    if need_check_sql:
                        sql.add_to_gained_items(acc_name, gained_item)
                    print('forecast_letter', forecast_letter)
                    google.write_google(forecast_letter, slot)

                    print('Roll is done')
                    global inventory_matrix
                    inventory_matrix = {}
                    roll_amount -= 1
                    ahk.mouse_actions('move', x=950, y=950)
                    ahk.mouse_actions('click')
                    time.sleep(1)

                    ahk.mouse_actions('move', x=1800, y=90)
                    ahk.mouse_actions('click')

                    #self._go_to_market()
                    #time.sleep(3)
#
                    #ahk.mouse_actions('move', x=400, y=180)
                    #ahk.mouse_actions('click')
                    #time.sleep(3)
#
                    #new_item_position = False
#
                    #for _ in range(3):
                    #    new_item_position = image.get_gained_item_slot()
                    #    if new_item_position:
                    #        print('Найдена выпавшная шмотка')
                    #        break
#
                    #    ahk.mouse_actions('move', x=1605, y=530)
#
                    #    self._wheel_inventory_down()
#
                    #if image.get_amount_of_slots() < 30:
                    #    print('Колличество слотов меньше 30')
                    #    if new_item_position:
                    #        print(f"Позиция выпавшей шмотки {new_item_position}")
#
                    #        y, x = new_item_position
                    #        ahk.mouse_actions('move', x=1450+(x*100), y=350+(y*100))
                    #        ahk.mouse_actions('click')
                    #        time.sleep(4)
#
                    #        minimal_price = image.get_minimal_price()
                    #        if minimal_price:
                    #            print(f'Минимальная цена получена {minimal_price}')
#
                    #            if minimal_price > 10:
                    #                print("Миинимальная цена больше 10")
                    #                minimal_price -= 1
                    #            self.make_new_price(minimal_price)
                    #            self.confirm_new_price()
#
                    #        else:
                    #            print("Не удалось получить минимальную цену")
#
                    #        self._close_market()
                    #        time.sleep(3)
                    #else:
                    #    print("Колличество слотов 30")

                    end_time = time.time()

                    wasted_time = end_time - start_time

                    decrease_roll_amount(acc_name)

                    return items_on_market, accesory_items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time
        except Exception as e:
            TGNotifier.send_break_msg('Алхимка', acc_name, e)

    def check_neccesary_color_of_forecast(self, colors):
        color_of_forecast = self._check_color_of_forecast()
        if color_of_forecast is False:
            return False, color_of_forecast
        if color_of_forecast in colors:
            return True, color_of_forecast
        return False, color_of_forecast

    def _check_color_of_forecast(self):

        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\color_of_forecast.png', area_of_screenshot=(930, 547, 950, 564))
        img = cv2.imread(f'{PATH_TO_ALCHEMY}\\imgs\\color_of_forecast.png')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define the range of colors for each color
        lower_white = np.array([0, 0, 180], dtype=np.uint8)
        upper_white = np.array([360, 30, 255], dtype=np.uint8)

        lower_blue = np.array([80, 50, 50], dtype=np.uint8)
        upper_blue = np.array([130, 255, 255], dtype=np.uint8)

        lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
        upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

        lower_orange = np.array([10, 50, 50], dtype=np.uint8)
        upper_orange = np.array([20, 255, 255], dtype=np.uint8)

        # Threshold the image to get only the colors in the defined range
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Count the number of pixels for each color
        white_pixels = cv2.countNonZero(white_mask)
        yellow_pixels = cv2.countNonZero(yellow_mask)
        orange_pixels = cv2.countNonZero(orange_mask)
        blue_pixels = cv2.countNonZero(blue_mask)

        # Determine the dominant color
        dominant_color = max(white_pixels, yellow_pixels, orange_pixels, blue_pixels)

        # Return the corresponding number based on the dominant color
        if dominant_color == white_pixels:
            print("Цвет круга белый")
            return self.WHITE
        elif dominant_color == yellow_pixels:
            print("Цвет круга золотой")
            return self.GOLD
        elif dominant_color == orange_pixels:
            print("Цвет круга золотой")
            return self.GOLD
        elif dominant_color == blue_pixels:
            print("Цвет круга голубой")
            return self.BLUE


    def get_rid_of_junk_symbols(self, text):
        for i in text:
            if ':' in i:
                text.remove(i)
            elif '&' in i:
                text.remove(i)
            elif '.' in i:
                text.remove(i)
            elif '@' in i:
                text.remove(i)
            elif "'" in i:
                text.remove(i)
            elif "," in i:
                text.remove(i)
            elif "}" in i:
                text.remove(i)
            elif "!" in i:
                text.remove(i)
            elif "*" in i:
                text.remove(i)
            elif '"' in i:
                text.remove(i)
            elif "_" in i:
                text.remove(i)

        text = "".join(text).replace(' ', '').replace('\n', '').lower()
        return text

    def buy_neccesary_items(self, amount_of_neccesary_items, items_list, list_of_items_to_find_in, is_acessory=False):
        print(f'buy_neccesary_items is_accessory is {is_acessory}')
        self._go_to_market()
        time.sleep(1)

        if items_list is None or len(items_list) == 0:
            prices_and_goods = self._find_goods_and_prices(list_of_items_to_find_in, amount_of_neccesary_items, is_acessory)
            if is_acessory:
                global accesory_items_on_market
                accesory_items_on_market = prices_and_goods
            else:
                global items_on_market
                items_on_market = prices_and_goods
        else:
            ahk.mouse_actions('move', x=80, y=380)
            ahk.mouse_actions('click')

        counter = amount_of_neccesary_items

        if is_acessory:
            items_list = accesory_items_on_market
        else:
            items_list = items_on_market

        for i in items_list.items():
            if image.is_dead():
                self._go_to_market()
            self._check_if_need_go_to_find_menu()
            if counter == 0:
                break
            item_name = i[0]
            print(item_name)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')

            name_of_item = item_name.replace(' ', '')
            time.sleep(0.4)

            ahk.mouse_actions('type', text=name_of_item)
            time.sleep(0.4)

            x_cord_to_buy_item = 260

            need_to_double_click = True
            for name in LIST_OF_BLUE_ITEMS_THAT_IN_2ND_SLOT:
                if name.replace(' ', '').replace('\n', '').lower() == item_name.replace(' ', '').replace('\n', '').lower():
                    x_cord_to_buy_item = 1000
                    need_to_double_click = False
                    break
            if need_to_double_click:
                amount_of_clicks = 2
            else:
                amount_of_clicks = 1

            for y in range(amount_of_clicks):
                ahk.mouse_actions('move', x=x_cord_to_buy_item, y=300)
                ahk.mouse_actions('click')
            time.sleep(0.2)

            item_price = i[1]
            print(item_price)
            time.sleep(3)

            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\price.png', area_of_screenshot=(1100, 450, 1230, 490))

            try:
                сurrent_price = int(image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\price.png', is_digits=True))
            except:
                print('Не смог определить текущую цену шмотки, скипает')
                continue

            if сurrent_price <= item_price:
                if self._buy_item(сurrent_price) is False:
                    continue
                global diamonds_wasted
                global items_bought

                diamonds_wasted += сurrent_price
                items_bought[item_name] = сurrent_price

                counter -= 1

            else:
                if is_acessory:
                    accesory_items_on_market.update({item_name: сurrent_price})
                    accesory_items_on_market = self._sort_dict(accesory_items_on_market)

                else:
                    items_on_market.update({item_name: сurrent_price})
                    items_on_market = self._sort_dict(items_on_market)

        ahk.mouse_actions('esc')

    def _sort_dict(self, dict_for_sort):
            sorted_dict = {}
            sorted_keys = sorted(dict_for_sort, key=dict_for_sort.get)
            for w in sorted_keys:
                sorted_dict[w] = dict_for_sort[w]
            return sorted_dict

    def _find_goods_and_prices(self, list_to_find_in, amount, is_acessory):
        print(f'_find_goods_and_prices is_accessory {is_acessory}')
        def __sort_dict(dict_for_sort):
                sorted_dict = {}
                sorted_keys = sorted(dict_for_sort, key=dict_for_sort.get)
                for w in sorted_keys:
                    sorted_dict[w] = dict_for_sort[w]
                return sorted_dict

        if image.is_dead():
            self._go_to_market()

        prices_and_goods = {}

        is_market_open = False
        while is_market_open is False:
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_market_open.png', area_of_screenshot=(50, 377, 51, 379))
            color = image.get_main_color(f'{PATH_TO_ALCHEMY}\\imgs\\is_market_open.png')
            print(color)
            if not (250 < color[0] < 256) and not (250 < color[1] < 256) and not (250 < color[2] < 256) or \
                   (901 < color[0] < 110) and not (80 < color[1] < 100) and not (80 < color[2] < 110):
                ahk.mouse_actions('move', x=80, y=380)
                ahk.mouse_actions('click')
            else:
                is_market_open = True

        time.sleep(2)
        #if not is_acessory:
        #    list_to_find_in = ['Цербер', 'Кристальный Арбалет'] + list_to_find_in

        print(f'list_to_find_in {list_to_find_in}')

        counter = 0

        for i in list_to_find_in:
            skip = False
            while skip is False:
                self._check_if_need_go_to_find_menu()

                ahk.mouse_actions('move', x=800, y=280)
                ahk.mouse_actions('click')

                ahk.mouse_actions('move', x=150, y=190)
                ahk.mouse_actions('click')

                x_cord_to_buy_item = 260
                name_of_item = i.replace(' ', '')

                triple_click = True
                for name in LIST_OF_BLUE_ITEMS_THAT_IN_2ND_SLOT:
                    if name.replace(' ', '').replace('\n', '').lower() == name_of_item.replace(' ', '').replace('\n', '').lower():
                        x_cord_to_buy_item = 1000
                        triple_click = False
                        break

                ahk.mouse_actions('type', text=name_of_item)
                time.sleep(0.4)
                ahk.mouse_actions('move', x=x_cord_to_buy_item, y=300)

                if triple_click:
                    for _ in range(3):
                        ahk.mouse_actions('click')
                else:
                    ahk.mouse_actions('click')

                time.sleep(1.1)

                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\price.png', area_of_screenshot=(1100, 450, 1230, 490))

                price = image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\price.png', is_digits=True)

                try:
                    int(price)
                except:
                    print("Не смог определить цену шмотки")
                    break

                if is_acessory is False:
                    print('is_accesory False')
                    if int(price) == 10:
                        if self._buy_item(price) is False:
                            skip = True
                            continue
                        counter += 1
                        skip = False
                        if counter == amount:
                            return prices_and_goods
                        continue
                    else:
                        skip = True
                        continue

                if int(price) >= 10:
                    prices_and_goods.update({i: int(price)})
                    skip = True
                else:
                    print(f'Цена шмотки {price}. Скип')
                    skip = True

                print(prices_and_goods)

        prices_and_goods = __sort_dict(prices_and_goods)
        return prices_and_goods

    def _buy_item(self, price):
        time.sleep(4)
        for i in range(2):
            time.sleep(1)
            ahk.mouse_actions('move', x=900, y=470)
            ahk.mouse_actions('click')
            time.sleep(0.5*MULTIPLIER)

        time.sleep(2)
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\current_price.png', area_of_screenshot=(1625, 445, 1685, 500))

        try:
            current_price = int(image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\current_price.png', is_digits=True))
        except:
            print('Не удалось определить текущую цену')
            return False

        if int(price) < current_price:

            print('Текущая цена больше нужной')
            return False

        ahk.mouse_actions('move', x=900, y=470)
        ahk.mouse_actions('click')
        time.sleep(0.5*MULTIPLIER)

        ahk.mouse_actions('move', x=1100, y=920)
        ahk.mouse_actions('click')

        while image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_bought.png',
                             f'{PATH_TO_ALCHEMY}\\imgs\\item_bought.png',
                             need_for_taking_screenshot=True, area_of_screenshot=(1185, 300, 1275, 330)) is False:
            if image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_bought.png', False).replace(' ', '').replace('\n', '').lower() == 'неудача':
                break
            time.sleep(0.1)

        time.sleep(2)

        ahk.mouse_actions('move', x=930, y=900)
        ahk.mouse_actions('click')

    def _check_if_need_go_to_find_menu(self):
        def __go_to_find_menu():
            ahk.mouse_actions('move', x=170, y=180)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=80, y=385)
            ahk.mouse_actions('click')
        is_market_open = False
        while is_market_open is False:
            if image.is_dead():
                self._go_to_market()

            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_market_open.png', area_of_screenshot=(50, 377, 51, 379))
            color = image.get_main_color(f'{PATH_TO_ALCHEMY}\\imgs\\is_market_open.png')
            print(color)
            if not (250 < color[0] < 256) and not (250 < color[1] < 256) and not (250 < color[2] < 256):
                print('Вышел с меню поиска')
                __go_to_find_menu()
                time.sleep(1)
            else:
                is_market_open = True

    def _go_to_market(self):
        time.sleep(4)

        ahk.mouse_actions('move', x=1775, y=85)
        ahk.mouse_actions('click')
        time.sleep(1)


        ahk.mouse_actions('move', x=1780, y=335)
        ahk.mouse_actions('click')

        time.sleep(2)

    def choose_necceary_items_from_inventory(self, neccesary_items_and_colors, except_accesories=False,
                                             except_sharp=False, need_for_check_roll_items_name=True, items_list=None,
                                             accesory_items_list=None,tg=None, roll=None):
        global inventory_matrix
        cords_of_choosed_items = {}

        counter_x = 1
        counter_y = 1
        counter = 0
        for i in neccesary_items_and_colors.items():
            amount_of_items_to_choose = i[1]
            if counter > 0:
                try:
                    color = i[0]
                    if color != inventory_matrix[(counter_x, counter_y)]:
                        if counter_x > 4:
                            counter_x = 1
                            counter_y += 1
                            print('Скип')

                except:
                    pass

            if counter_x > 4:
                counter_x = 1
                counter_y += 1
                pass

            counter+=1
            for a in range(amount_of_items_to_choose):

                color = i[0]
                is_color_ok = False

                for key, value in inventory_matrix.items():
                    if value == color:
                        print(key)
                        counter_x = key[0]
                        counter_y = key[1]
                        inventory_matrix[key] = False
                        break

                while is_color_ok is False:
                    for b in range(4):
                        if (counter_x, counter_y) not in cords_of_choosed_items.items():

                            ahk.mouse_actions('move', x=1350+counter_x*100, y=200+counter_y*100)
                            ahk.mouse_actions('click')

                            collect_roll = self._check_item_in_inventory_color(row=(counter_x, counter_y), except_accesories=except_accesories,
                                                                               except_sharp=except_sharp,
                                                                               need_for_check_roll_items_name=need_for_check_roll_items_name)

                            inventory_matrix[(counter_x, counter_y)] = collect_roll
                            print(inventory_matrix)
                            if collect_roll == color:
                                for c in range(3):
                                    ahk.mouse_actions('click')
                                is_color_ok = True

                                cords_of_choosed_items[counter_x] = counter_y
                                counter_x += 1
                                if counter_x > 4:
                                    counter_x = 1
                                    counter_y += 1
                                break

                            if collect_roll == 'END':
                                ahk.mouse_actions('esc')
                                amount_of_items_to_craft = amount_of_items_to_choose - a
                                if color is self.GREEN:
                                    inventory_matrix = {}
                                    if self.craft_green_items(amount_of_items_to_craft) is False:
                                        print("Зеленая шмотка была скрафчена, но бот ее не заметил")
                                        return 'GREEN ERROR'
                                    global adena_wasted
                                    adena_wasted += 50000
                                    self._go_to_alchemy()
                                elif color is self.BLUE:
                                    inventory_matrix = {}
                                    self.buy_neccesary_items(amount_of_items_to_craft, items_list, LIST_OF_RARE_ITEMS)
                                    sort_inventory()
                                    self._go_to_alchemy()
                                elif color is self.PLUS_1_ACCESORY:
                                    inventory_matrix = {}
                                    self.craft_plus_1_accesories(amount_of_items_to_craft, accesory_items_list)
                                    sort_inventory()
                                    self._go_to_alchemy()
                                elif color is self.PLUS_2_ACCESORY:
                                    inventory_matrix = {}
                                    self.craft_plus_2_accesories(amount_of_items_to_craft, accesory_items_list)
                                    sort_inventory()
                                    self._go_to_alchemy()

                                return False
                            counter_x += 1
                        else:
                            counter_x += 1

                        if counter_x > 4:
                            counter_x = 1
                            counter_y += 1
        if roll == '66':
            if not image.is_5th_slot_in_alchemy_not_empty():
                ahk.mouse_actions('esc')
                self._go_to_alchemy()
                inventory_matrix = {}
                return False
        elif roll == '80':
            if image.check_4th_slot_empty():
                ahk.mouse_actions('esc')
                sort_inventory()
                self._go_to_alchemy()
                inventory_matrix = {}
                return False
        return True

    def _check_item_in_inventory_color(self, row, except_accesories=True, except_sharp=False, need_for_check_roll_items_name=True):
        def __check_is_item_appropriate():
            x = row[0]
            y = row[1]

            print(x)
            print(y)
            if y > 6:
                print('Посмотрел весь инвентарь')
                return False

            elif image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_equiped.png',
                                             f'{PATH_TO_ALCHEMY}\\imgs\\item_is_equiped.png',
                                             need_for_taking_screenshot=True, area_of_screenshot=(1400+x*100+1-100, 260+y*100+1-100,
                                                                                                  1425+x*100+1-100, 290+y*100+1-100),
                                             threshold=0.8) is True:
                print('Предмет экипирован')
                return False

        y = row[1]*100
        try:
            time.sleep(0.5)
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\item_in_inventory_name.png', area_of_screenshot=(1400, 50+y, 1800, 162+y+5))
            item_name = image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\item_in_inventory_name.png', is_digits=False).split('\n')
            print('Название шмотки без обработки', item_name)
        except:
            return False

        if __check_is_item_appropriate() is False:
            print(item_name, 'Нельзя положить')
            return 'END'
        try:
            for i in item_name:
                if '&' in i:
                    item_name.remove(i)
                elif '.' in i:
                    item_name.remove(i)
                elif '@' in i:
                    item_name.remove(i)
                elif "'" in i:
                    item_name.remove(i)
                elif "," in i:
                    item_name.remove(i)
                elif "}" in i:
                    item_name.remove(i)
                elif "!" in i:
                    item_name.remove(i)
                elif "*" in i:
                    item_name.remove(i)
                elif '"' in i:
                    item_name.remove(i)
                elif "_" in i:
                    item_name.remove(i)
                elif "=" in i:
                    item_name.remove(i)
                elif "®" in i:
                    item_name.remove(i)
                elif "’" in i:
                    item_name.remove(i)
                elif ")" in i:
                    item_name.remove(i)
                elif "(" in i:
                    item_name.remove(i)
                elif "0" in i:
                    item_name.remove(i)
                elif "!" in i:
                    item_name.remove(i)
                elif "?" in i:
                    item_name.remove(i)
                elif ">" in i:
                    item_name.remove(i)
        except Exception as e:
            print(e)
            print("Скип шмотки и")
            return False

        item_name = "".join(item_name).replace(' ', '').replace('\n', '').lower()
        item_name = item_name.replace('%', '').replace('.', '').replace('{', '').replace('°', '').replace(',', '').replace('“','').replace('.','').replace('№', '')

        print('Название шмотки ', item_name)

        if 'гермункус' in item_name:
            print('Гермункус')
            return False

        image.delete_all_colors_except_blue(f'{PATH_TO_ALCHEMY}\\imgs\\item_in_inventory_name.png')
        print('Blue template for item matching ready')
        image.delete_all_colors_except_green(f'{PATH_TO_ALCHEMY}\\imgs\\item_in_inventory_name.png')
        print('Green template for item matching ready')
        image.delete_all_colors_except_red(f'{PATH_TO_ALCHEMY}\\imgs\\item_in_inventory_name.png')
        print('Red template for item matching ready')

        try:
            if except_sharp is True:
                if '+' in item_name.replace('\n', ''):
                    print(item_name, 'Заточенная')
                    return False
        except:
            pass

        if self._is_item_color_green('green.png'):
            print('Green')
            item_name = image.image_to_string('green.png', is_digits=False)
            print(f'item name from green template is {item_name}')

            if __check_is_item_appropriate() is False:
                print(item_name, 'Нельзя положить')
                return 'END'

            list_of_sharp = ('+', '1', '2', '4', '5', '6', '7', '8', '9', '10', '11')
            for c in list_of_sharp:
                if c in item_name:
                    print('Зеленая точенная ', item_name)
                    return False
            return self.GREEN

        else:
            print('item is not green')

        if self._is_item_color_blue('blue.png'):
            print('Blue')

            item_name = image.image_to_string('blue.png', is_digits=False)
            print(f'item name from blue template is {item_name}')

            if except_accesories is True:
                if item_name.replace('\n', '') in ACESSORIES_LIST:
                    print(item_name, 'Бижа')
                    return False
            if __check_is_item_appropriate() is False:
                print(item_name, 'Нельзя положить')
                return 'END'
            print('item_name is ', item_name)
            print('Название шмотки ', item_name)
            found_item = False
            LIST_OF_ACCESORIES_WORDS = ('кольцо', 'ожерелье', 'серьга', 'пояс', 'браслет', 'ожёрелье', 'глаз')
            LIST_OF_PIECE_WORDS = ('авадон', 'молнии', 'зубе', 'кронвист')
            for i in LIST_OF_ACCESORIES_WORDS:
                if i in item_name.replace('\n', '').lower():
                    if '+1' in item_name.replace('\n', '').lower():
                        print('+1 Accessory')
                        return self.PLUS_1_ACCESORY

                    elif '+2' in item_name.replace('\n', '').lower():
                        print('+2 Accessory')
                        return self.PLUS_2_ACCESORY

                    elif '+3' in item_name.replace('\n', '').lower():
                        print('+3 Accessory')
                        return self.PLUS_3_ACCESORY
                    else:
                        print('+0 Accessory')
                        return self.PLUS_0_ACCESORY
            print(item_name, 'is not accessory')
            for i in LIST_OF_PIECE_WORDS:
                if i in item_name.replace('\n', '').lower():
                    if '8' in item_name.replace('\n', '').lower():
                        return self.PIECE
                    else:
                        return self.PIECE_NOT_PLUS_8

            for c in LIST_OF_RARE_ITEMS_FOR_ALCHEMY:
                if SequenceMatcher(None, item_name.replace(' ', '').replace('\n', '').replace('—', '-').lower(), c.replace(' ', '').lower()).ratio() > 0.65:
                    found_item = True
                    break

            for d in ADDITIONAL_GOOD_RARE_ITEMS_LIST:
                if SequenceMatcher(None, item_name.replace(' ', '').replace('\n', '').replace('—', '-').lower(), d.replace(' ', '').replace('\n', '').replace('—', '-').lower()).ratio() > 0.83:
                    found_item = True
                    break

            if found_item is False:
                print(item_name, 'нету в списке')
                return False

            for с in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_'):
                if с in item_name.replace('\n', ''):
                    print(item_name, 'Заточенная')
                    return False

            return self.BLUE
        else:
            print('item is not blue')

        if self._is_item_color_red('red.png'):
            if '+' in item_name:
                LIST_OF_ACCESORIES_WORDS = ('кольцо', 'ожерелье', 'пояс', 'серьга', 'браслет')
                for i in LIST_OF_ACCESORIES_WORDS:
                    if i in item_name:
                        if '1' in item_name:
                            return self.PLUS_1_RED_ACCESORY
                        elif '2' in item_name:
                            return self.PLUS_2_RED_ACCESORY
                        elif '3' in item_name:
                            return self.PLUS_3_RED_ACCESORY
                        elif '4' in item_name:
                            return self.PLUS_4_RED_ACCESORY
                        elif '5' in item_name:
                            return self.PLUS_5_RED_ACCESORY
                        else:
                            return self.PLUS_0_RED_ACCESORY
            return self.RED
        else:
            print('Не зеленая и не синяя')
            return False

    def _is_item_color_green(self, img):
        try:
            color = image.get_main_color(img)
            print(color)
            if color:
                if (0 <= color[0] <= 40) and (140 <= color[1] <= 180) and (50 <= color[2] <= 90):
                    print(color)
                    print('items is green')
                    return True
                return False
            else:
                print('Не смог определить зеленая шмотка или нет. Место: _is_item_color_green')
        except Exception as e:
            print('Error: place: _is_item_color_green\n', e)

    def _is_item_color_blue(self, img):
        try:
            color = image.get_main_color(img)
            print(color)
            if color:
                if (5 <= color[0] <= 35) and (100 <= color[1] <= 130) and (170 <= color[2] <= 256):
                    if image.image_to_string(img, is_digits=False):
                        return True
                return False
            else:
                print('Не смог определить синяя шмотка или нет. Место: _is_item_color_blue')
        except Exception as e:
            print('Error: place: _is_item_color_blue\n', e)

    def _is_item_color_red(self, img):
        try:
            color = image.get_main_color(img)
            print(color)
            if color:
                if (140 < color[0] < 255) and (20 < color[1] < 45) and (45 < color[2] < 70):
                    if image.image_to_string(img, is_digits=False):
                        return True
                return False
            else:
                print('Не смог определить красная шмотка или нет. Место: _is_item_color_red')
        except Exception as e:
            print('Error: place: _is_item_color_red\n', e)

    def check_items_price(self, slots, list_of_appropriate_roll_items, red_check, need_for_totaling_prices=False,
                          need_check_sql=False, hwnd=None, color_of_forecast=None, is_888=False, is_80=False, need_sequence_matching=False,
                          need_find_by_image=False, roll=None, need_check_symbol=False):

        price = 0
        try:
            if list_of_appropriate_roll_items is not None:
                with open(list_of_appropriate_roll_items, 'r', encoding='utf-8') as items:
                    list_of_items = items.read().replace(' ', '').lower().split('\n')
            print(list_of_items)
        except:
            print("Не удалось открыть список шмоток")
            return False

        if roll == '40':
            time.sleep(0.4)
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_1_slot_red.png', area_of_screenshot=(775, 488, 876, 490))
            if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_1_slot_red.png') is True:
                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_red.png', area_of_screenshot=(875, 488, 876, 490))

                if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_red.png') is True:
                    image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_purple.png', area_of_screenshot=(975, 488, 976, 490))

                    if self._check_purple(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_purple.png') is True:
                        print('Есть фиол шмотка в 3 слоте')
                        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_4_slot_purple.png', area_of_screenshot=(1075, 488, 1076, 490))

                        if self._check_purple(f'{PATH_TO_ALCHEMY}\\imgs\\is_4_slot_purple.png') is True:
                            print('Есть фиол шмотка в 4 слоте')
                            if need_check_symbol is False:
                                return 5000
                        else:
                            print('Нет фиол шмотки в 4 слотенн')
                            return False
                    else:
                        print('Нет фиол шмотки в 3 слоте')
                        return False
                else:
                    print('Нет красной шмотки во 2 слоте')
            else:
                print('Нет красной шмотки в 1 слоте')
                return False

        elif roll == '50':
            time.sleep(0.2)
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_1_slot_red.png', area_of_screenshot=(775, 488, 876, 490))
            if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_1_slot_red.png') is True:
                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_purple.png', area_of_screenshot=(874, 488, 876, 490))
                if self._check_purple(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_purple.png') is True:
                    image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_purple.png', area_of_screenshot=(974, 488, 976, 490))
                    print('Есть фиол шмотка во 2 слоте')
                    if self._check_purple(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_purple.png') is True:
                        print('Есть фиол шмотка в 3 слоте')
                        if need_check_symbol is False:
                            return 5000
                    else:
                        print('Нет фиол шмотки в 3 слоте')
                        return False
                else:
                    print('Нет фиол шмотки во 2 слоте')
                    return False
            else:
                print('Нет красной шмотки в 1 слоте')
                return False

        elif roll == '50_plus':
            time.sleep(0.2)
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_1_slot_red.png', area_of_screenshot=(775, 488, 876, 490))
            if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_1_slot_red.png') is True:
                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_purple.png', area_of_screenshot=(874, 488, 876, 490))
                if self._check_purple(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_purple.png') is True:
                    image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_purple.png', area_of_screenshot=(974, 488, 976, 490))
                    print('Есть фиол шмотка во 2 слоте')
                    if self._check_purple(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_purple.png') is True:
                        print('Есть фиол шмотка в 3 слоте')
                        if need_check_symbol is False:
                            return 5000
                    else:
                        print('Нет фиол шмотки в 3 слоте')
                        return False
                else:
                    print('Нет фиол шмотки во 2 слоте')
                    return False
            else:
                print('Нет красной шмотки в 1 слоте')
                return False

        if roll == '80red':
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_red.png', area_of_screenshot=(975, 488, 976, 490))
            if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_red.png') is True:
                print('Есть красная шмотка в 3 слоте')
                roll = '66'
            else:
                return False
        if red_check:
            if is_80:
                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_red.png', area_of_screenshot=(975, 488, 976, 490))
                if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_red.png') is True:
                    print('Есть красная шмотка в 3 слоте')
                else:
                    return False
            else:
                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_4_slot_red.png', area_of_screenshot=(1075, 488, 1076, 490))
                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_5_slot_red.png', area_of_screenshot=(1175, 488, 1176, 490))

                if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_4_slot_red.png') is True:
                    if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_5_slot_red.png') is True:
                        if is_888:
                            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_red.png', area_of_screenshot=(975, 488, 976, 490))
                            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_red.png', area_of_screenshot=(875, 488, 876, 490))

                            if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_3_slot_red.png') is True:
                                if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_2_slot_red.png') is True:
                                    print("Есть красные шмотки в 2-5 слотах")
                                else:
                                    return False
                            else:
                                return False
                        print('Есть красные шмотки в 4 и 5 слоте')
                    else:
                        return False
                else:
                    return False

        if is_80:
            if color_of_forecast is self.BLUE:
                slots = [3, 2]
            elif color_of_forecast is self.GOLD:
                slots = [3, 2]

        if is_888:
            if color_of_forecast is self.BLUE:
                slots = [2, 3]
            elif color_of_forecast is self.GOLD:
                slots = [2, 3]
        for i in slots:
            if need_find_by_image:
                if is_80:
                    if color_of_forecast is self.BLUE and i == 2:
                        roll = '66'

                if roll == '50_plus' and i == 2:
                    roll = '50'

                mypath = f'{PATH_TO_ALCHEMY}\\imgs\\roll_{roll}_images\\'
                roll_images = []
                if roll != '00':
                    roll_images = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                    print(roll_images)
                if self.check_if_item_image_in_forecast(i, roll_images, roll) is True:
                    print('Найдена нужная шмотка в ', i, 'слоте')
                else:
                    return False
            if roll == '000':
                if i == 2:
                    with open(f'{PATH_TO_ALCHEMY}\\roll_000_items.txt', 'r', encoding='utf-8') as roll_000_items:
                        list_of_items = roll_000_items.read().replace(' ', '').lower().split('\n')

                if i == 1:
                    with open(f'{PATH_TO_ALCHEMY}\\rol_00_items.txt', 'r', encoding='utf-8') as roll_00_items:
                        list_of_items = roll_00_items.read().replace(' ', '').lower().split('\n')

            ahk.mouse_actions('move', x=630+(i*100), y=500)
            ahk.mouse_actions('click')
            item_name = self._check_item_name_in_forecast(is_80, is_888, roll).replace(' ', '').lower().split('\n')
            for c in item_name:
                if ':' in c:
                    item_name.remove(c)
                elif '&' in c:
                    item_name.remove(c)
                elif '.' in c:
                    item_name.remove(c)
                elif '@' in c:
                    item_name.remove(c)
                elif "'" in c:
                    item_name.remove(c)
                elif "," in c:
                    item_name.remove(c)
                elif "}" in c:
                    item_name.remove(c)
                elif "!" in c:
                    item_name.remove(c)
                elif "*" in c:
                    item_name.remove(c)
                elif '"' in c:
                    item_name.remove(c)
                elif "<" in c:
                    item_name.remove(c)
                elif ">" in c:
                    item_name.remove(c)
                elif "^" in c:
                    item_name.remove(c)
                elif "®" in c:
                    item_name.remove(c)
                elif "_" in c:
                    item_name.remove(c)
            item_name = "".join(item_name).replace(' ' , '')
            print(item_name)
            if is_80:
                if i == 3:
                    if color_of_forecast is self.GOLD:
                        with open(f'{PATH_TO_ALCHEMY}\\roll_80_888_items.txt', 'r', encoding='utf-8') as roll_888_80_items:
                            list_of_items = roll_888_80_items.read().replace(' ', '').lower().split('\n')
                    else:
                        with open(f'{PATH_TO_ALCHEMY}\\roll_80_items.txt', 'r', encoding='utf-8') as roll_80_items:
                            list_of_items = roll_80_items.read().replace(' ', '').lower().split('\n')
                elif i == 2:
                    with open(f'{PATH_TO_ALCHEMY}\\rol_66_items.txt', 'r', encoding='utf-8') as roll_888_80_items:
                        list_of_items = roll_888_80_items.read().replace(' ', '').lower().split('\n')
            if need_sequence_matching:
                is_item_in_list = False
                print(list_of_items)
                for roll_item in list_of_items:
                    if SequenceMatcher(a=item_name.lower(), b=roll_item.lower().replace(' ', '')).ratio() > 0.7:
                        if item_name.lower()[0:2] == roll_item.lower().replace(' ', '')[0:2]:
                            print(item_name, 'in list')
                            is_item_in_list = True
                            break
                if is_item_in_list is False:
                    return False
            else:
                print(list_of_items)
                if item_name.lower().replace(' ', '') in list_of_items:
                    print(item_name, 'IN list')
                else:
                    if roll == '000':
                        if i == 1:
                            print('Шмотка не в списке 00, проверяет цену')
                    if is_80:
                        if color_of_forecast is self.GOLD:
                            continue
                        else:
                            return False
                    else:
                        return False
            if need_check_sql:
                for c in GAINED_ITEMS:
                    if SequenceMatcher(a=c,b=item_name).ratio() > 0.95:
                        if c[0:2] == item_name[0:2]:
                            print(item_name, ' уже есть на сервере')
                            acc_name = self.get_window_name(hwnd)
                            return False
                if item_name in LESS_100_ITEMS:
                    print(item_name, ' стоит меньше 100')
                    return False

            print(item_name)

            ahk.mouse_actions('press')
            ahk.mouse_actions('move', x=775, y=770)
            ahk.mouse_actions('click')
            time.sleep(4)

            ahk.mouse_actions('move', x=700, y=470)
            ahk.mouse_actions('click')
            time.sleep(4)

            price = self._check_if_item_on_market(item_name)

            if len(slots) > 1:
                ahk.mouse_actions('esc')
                time.sleep(0.1)
                self._open_forecast()
                time.sleep(0.1)
            if price is False:
                print('Шмотка не найдена')
                continue
            if roll == '000':
                print('Цена шмотки', price)
                if i == 1:
                    if price >= ROLL_000_MINIMAL_PRICE_1ST_SLOT:
                        return True
                if i == 2:
                    if price >= ROLL_000_MINIMAL_PRICE_2ND_SLOT:
                        return True
                    elif price >= ROLL_000_MINIMAL_PRICE_2ND_SLOT_FOR_CHECK_1ST_SLOT:
                        continue
            if price >= MINIMAL_PRICE_FOR_ROLL:
                print("Шмотка подходит под нужное описание вот цена ", price)
            else:
                if need_check_sql:
                    sql.add_to_less_100_items(hwnd, item_name)
                    print('Цена шмотки меньше чем нужно, Цена ', price)
                return False
            if is_80:
                if color_of_forecast is self.GOLD:
                    return True
        return True
    def _check_red(self, image_path):
        image = cv2.imread(image_path)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # устанавливаем диапазон красного цвета в HSV
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        lower_red_2 = np.array([170, 50, 50])
        upper_red_2 = np.array([180, 255, 255])
        # создаем маску для выделения красного цвета в изображении
        mask1 = cv2.inRange(hsv_image, lower_red, upper_red)
        mask2 = cv2.inRange(hsv_image, lower_red_2, upper_red_2)
        mask = cv2.bitwise_or(mask1, mask2)
        # вычисляем количество пикселей, соответствующих красному цветунн
        num_red_pixels = cv2.countNonZero(mask)
        # если количество пикселей больше некоторого порога,
        # то считаем, что на изображении есть красный цвет
        if num_red_pixels >= 1:
            return True
        else:
            return False
    def _check_purple(self, image_path):
        image = cv2.imread(image_path)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # устанавливаем диапазон красного цвета в HSV
        lower_purple = np.array([70, 40, 120])
        upper_purple = np.array([240, 150, 255])
        lower_purple_2 = np.array([10, 10, 40])
        upper_purple_2 = np.array([110, 110, 110])
        # создаем маску для выделения красного цвета в изображении
        mask1 = cv2.inRange(hsv_image, lower_purple, upper_purple)
        mask2 = cv2.inRange(hsv_image, lower_purple_2, upper_purple_2)
        mask = cv2.bitwise_or(mask1, mask2)
        # вычисляем количество пикселей, соответствующих красному цветунн
        num_purple_pixels = cv2.countNonZero(mask)
        # если количество пикселей больше некоторого порога,
        # то считаем, что на изображении есть красный цвет
        if num_purple_pixels >= 1:
            return True
        else:
            return False

    def check_which_slots_are_red(self, slots):
        global red_slots
        for i in range(5):
            check_red_slot = Thread(target=self._check_red, args=(i,))
            check_red_slot.start()
        red_slots = sorted(red_slots)
        if slots == red_slots:
            return True


    def _check_if_item_on_market(self, item_name):
        self.set_neccesary_sharp(item_name.replace('\n', '').replace(' ', ''))
        time.sleep(2)
        try:
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\item_price_on_market.png',
                                      area_of_screenshot=(1110, 445, 1250, 485))
            price = image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\item_price_on_market.png', is_digits=True)
            print('Цена шмотки, ', price)
            if price:
                return int(price)

            return 500
        except:
            return False

    def check_if_item_image_in_forecast(self, slot, images_list, roll):
        time.sleep(0.2)
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\item_on_forecast_image.png',
                              area_of_screenshot=(580+(slot*100), 440, 685+slot*100, 555))
        threshold = 0.7
        item_on_forecast_image = cv2.imread('item_on_forecast_image.png')
        if roll == '00':
            global template_list_00
            images_list = template_list_00
            threshold = 0.8
        print(images_list)
        for i in images_list:
            if roll == '00':
                #print(i)
                res = cv2.matchTemplate(item_on_forecast_image, i, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    print("Найдено совпадение")
                    return True
            else:
                if image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\item_on_forecast_image.png',
                                  f'{PATH_TO_ALCHEMY}\\imgs\\roll_{roll}_images\\{i}', need_for_taking_screenshot=False,
                                  threshold=threshold) is True:
                    print(i, 'found')
                    return True
                else:
                    print(i, 'not found')
        return False


    def set_neccesary_sharp(self, item_name):
        def __set_sharp(start_drag, end_drag):
            start_x = 315
            end_x = 1770
            ahk.mouse_actions('move', x=start_x, y=250)
            ahk.mouse_actions('press down')
            ahk.mouse_actions('move', x=start_drag, y=0, relative=True)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=end_x, y=250)
            ahk.mouse_actions('press down')
            ahk.mouse_actions('move', x=-end_drag, y=0, relative=True)
            ahk.mouse_actions('click')

        if '+' not in item_name:
            return

        ahk.mouse_actions('move', x=480, y=300)
        ahk.mouse_actions('click')

        sharp = item_name[1]

        if sharp == '1':
            __set_sharp(start_drag=130, end_drag=1325)
        elif sharp == '2':
            __set_sharp(start_drag=265, end_drag=1190)
        elif sharp == '3':
            __set_sharp(start_drag=395, end_drag=1060)
        elif sharp == '4':
            __set_sharp(start_drag=530, end_drag=925)
        elif sharp == '5':
            __set_sharp(start_drag=660, end_drag=795)
        elif sharp == '6':
            __set_sharp(start_drag=795, end_drag=660)
        elif sharp == '7':
            __set_sharp(start_drag=925, end_drag=530)
        elif sharp == '8':
            __set_sharp(start_drag=1060, end_drag=395)
        elif sharp == '9':
            __set_sharp(start_drag=1190, end_drag=265)
        elif sharp == '10':
            __set_sharp(start_drag=1325, end_drag=130)
        elif sharp == '11':
            __set_sharp(start_drag=1455, end_drag=0)


        ahk.mouse_actions('move', x=1100, y=955)
        ahk.mouse_actions('click')

        time.sleep(4)

    def _check_item_name_in_forecast(self, is_888, is_80, roll):
        time.sleep(0.4)
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\item_name_in_forecast.png', area_of_screenshot=(730, 380, 1130, 440))

        if is_80 or is_888:
            image.black_and_white_80_888(f'{PATH_TO_ALCHEMY}\\imgs\\item_name_in_forecast.png', roll)
            item_name = pytesseract.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\item_name_in_forecast.png', lang='rus', config='--psm 3').split('\n')
        else:
            cv2image = cv2.imread(f'{PATH_TO_ALCHEMY}\\imgs\\item_name_in_forecast.png')
            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            invert = 255 - thresh

            item_name = pytesseract.image_to_string(invert, lang='rus', config='--psm 3').split('\n')

        for i in item_name:
            if ':' in i:
                item_name.remove(i)
            elif '&' in i:
                item_name.remove(i)
            elif '.' in i:
                item_name.remove(i)
            elif '@' in i:
                item_name.remove(i)
            elif "'" in i:
                item_name.remove(i)
            elif "," in i:
                item_name.remove(i)
            elif "}" in i:
                item_name.remove(i)
            elif "!" in i:
                item_name.remove(i)
            elif "*" in i:
                item_name.remove(i)
            elif '"' in i:
                item_name.remove(i)
            elif ")" in i:
                item_name.remove(i)

            item_name = "".join(item_name).replace(' ' , '')

            return item_name

    def _reset_roll(self):
        ahk.mouse_actions('move', x=230, y=950)
        time.sleep(0.2)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1070, y=700)
        time.sleep(0.2)
        ahk.mouse_actions('click')

    def _open_forecast(self):
        ahk.mouse_actions('y')

    def _repeat_forecast(self):
        for i in range(2):
            ahk.mouse_actions('y')


    def _start_roll(self):
        time.sleep(1)
        ahk.mouse_actions('move', x=1400, y=930)
        ahk.mouse_actions('click')
        time.sleep(1)
        if image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_inventoy_is_overflow_in_alchemy.png',
                          f'{PATH_TO_ALCHEMY}\\imgs\\inventoy_is_overflow_in_alchemy.png',
                          need_for_taking_screenshot=True, area_of_screenshot=(540, 150, 1315, 620),
                          threshold=0.8) is True:
            return False
        ahk.mouse_actions('move', x=1070, y=700)
        ahk.mouse_actions('click')
        time.sleep(1)

        ahk.mouse_actions('move', x=1200, y=700)
        ahk.mouse_actions('click')
        time.sleep(1)

    def _get_slot_and_name_of_item_that_gained(self):
        x = 225
        for i in range(5):
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\gained_slot.png', area_of_screenshot=(x-2, 538, x+2, 542))
            color = image.get_main_color(f'{PATH_TO_ALCHEMY}\\imgs\\gained_slot.png')
            print('color is ', color)
            if (25 < color[0] < 256) and (50 < color[1] < 256) and (65 < color[2] < 256):
                ahk.mouse_actions('move', x=x+30, y=540)
                ahk.mouse_actions('click')
                time.sleep(0.6)
                image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\name_of_gained_item.png', area_of_screenshot=(730, 310, 1130, 400))

                image.delete_all_colors_except_green(f'{PATH_TO_ALCHEMY}\\imgs\\name_of_gained_item.png')
                image.delete_all_colors_except_blue(f'{PATH_TO_ALCHEMY}\\imgs\\name_of_gained_item.png')
                image.delete_all_colors_except_red(f'{PATH_TO_ALCHEMY}\\imgs\\name_of_gained_item.png')

                image_string = f'{PATH_TO_ALCHEMY}\\imgs\\name_of_gained_item.png'

                if len(image.image_to_string('green.png', is_digits=False)) > 8:
                    image_string = 'green.png'
                    print('цвет выпавшей шмотки зеленый')

                elif len(image.image_to_string('blue.png', is_digits=False)) > 8:
                    image_string = 'blue.png'
                    print('Цвет выпавшей шмотки синий')

                elif len(image.image_to_string('red.png', is_digits=False)) > 8:
                    image_string = 'red.png'
                    print('Цвет выпавшей шмотки красный')

                else:
                    print('Цвет выпавшей шмотки белый')

                item_name = pytesseract.image_to_string(image_string, lang='rus', config='--psm 6').lower().split('\n')

                junk_symbols = ('.', ',', '|', '"', "'", '_', '>', '<', '№', '!', '@', '#',
                                '$', '%', '^', '&', '*', '=', '}', '{', ';', '?', '/', '\\',
                                'аа', 'бб', 'вв', 'гг', 'дд', 'ее', 'жж', 'зз', 'ии', 'йй',
                                'кк', 'лл', 'мм', 'нн', 'оо', 'пп', 'рр', 'сс', 'тт', 'уу',
                                'фф', 'хх', 'цц', 'чч', 'шш', 'щщ', 'яя')

                item_name_ready = ''

                print('item name not ready is', item_name)

                for c in item_name:
                    for j in junk_symbols:
                        if j in c:
                            c = ''
                            break
                    item_name_ready += c

                slot = i
                return item_name_ready, slot

            x += 285
        return '', 1

    def is_diamonds_in_forecast(self):
        if image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\forecast_items.png', f'{PATH_TO_ALCHEMY}\\imgs\\cristal.png',
                          need_for_taking_screenshot=True, area_of_screenshot=(500, 440, 1190, 550), threshold=0.785) is True:
            print('Diamonds Found')
            return True
        return False

    def craft_green_items(self, amount):
        global green_item_crafted

        if green_item_crafted:
            return False

        self._go_to_craft_menu()
        for i in range(amount):
            time.sleep(1)
            ahk.mouse_actions('move', x=1670, y=940)
            ahk.mouse_actions('click')
            overflow = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_inventory_overflow_in_craft.png',
                                      f'{PATH_TO_ALCHEMY}\\imgs\\inventoy_is_overflow_in_craft.png',
                                      need_for_taking_screenshot=True)

            if overflow:
                return False
            time.sleep(5)

            ahk.mouse_actions('move', x=930, y=950)
            ahk.mouse_actions('click')

        ahk.mouse_actions('esc')

    def _go_to_craft_menu(self):
        ahk.mouse_actions('move', x=1775, y=85)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1680, y=350)
        ahk.mouse_actions('click')

        time.sleep(1)
        ahk.mouse_actions('move', x=650, y=190)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')

    def craft_plus_1_accesories(self, amount, accesory_items_list):
        self.buy_neccesary_items(amount, accesory_items_list, ACESSORIES_LIST, is_acessory=True)
        accessory_shapred = False
        while accessory_shapred is False:
            if self._open_sharp_menu() is False:
                self._close_sharp_menu()
            if self._put_items_in_sharp_scrol(amount) is not False:
                accessory_shapred = True
    def craft_plus_2_accesories(self, amount, accesory_items_list):
        self.buy_neccesary_items(amount, accesory_items_list, ACESSORIES_LIST, is_acessory=True)
        accessory_shapred = False

        while accessory_shapred is False:
            if self._open_sharp_menu() is False:
                self._close_sharp_menu()
            if self._put_items_in_sharp_scrol(amount, True) is not False:
                accessory_shapred = True


    def _open_sharp_menu(self):
        ahk.mouse_actions('i')

        ahk.mouse_actions('move', x=1350, y=440)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')
        time.sleep(1.5)
        while image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_filter_selected.png',
                             f'{PATH_TO_ALCHEMY}\\imgs\\filter_is_selected.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(1755, 250, 1805, 310), threshold=0.6) is True:
            ahk.mouse_actions('move', x=1600, y=280)
            ahk.mouse_actions('click')
            time.sleep(0.5)
        time.sleep(1.5)

        while image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_filter_selected.png',
                             f'{PATH_TO_ALCHEMY}\\imgs\\filter_is_selected_half.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(1750, 720, 1810, 785), threshold=0.6) is False:
            ahk.mouse_actions('move', x=1600, y=750)
            ahk.mouse_actions('click')
            time.sleep(0.5)
            #ahk.mouse_actions('move', x=1600, y=500)
            #ahk.mouse_actions('wheel')
            #time.sleep(1.5)

        ahk.mouse_actions('wheel_up')
        time.sleep(1.5)
        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')
        time.sleep(0.5)
        if self._find_and_open_accessory_sharp_scroll() is False:
            return False
        time.sleep(1.5)
        ahk.mouse_actions('move', x=1050, y=180)
        ahk.mouse_actions('click')

        time.sleep(0.5)
    def _close_sharp_menu(self):
        ahk.mouse_actions('i')

        ahk.mouse_actions('move', x=1340, y=440)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1050, y=180)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')
        while image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_filter_selected.png',
                             f'{PATH_TO_ALCHEMY}\\imgs\\filter_is_selected.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(1755, 250, 1805, 310), threshold=0.6) is False:
            ahk.mouse_actions('move', x=1600, y=280)
            ahk.mouse_actions('click')
            time.sleep(0.5)
        ahk.mouse_actions('move', x=1600, y=280)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('move', x=1350, y=720)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('esc')

    def _exit_from_sharp_scroll(self):
        ahk.mouse_actions('move', x=1300, y=180)
        ahk.mouse_actions('click')
        time.sleep(1)

        ahk.mouse_actions('move', x=1785, y=180)
        ahk.mouse_actions('click')
        time.sleep(1)

    def _find_and_open_accessory_sharp_scroll(self):
        time.sleep(0.5)
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\inventory.png',area_of_screenshot=(1390, 240, 1800, 770))

        scroll_cords = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\inventory.png', f'{PATH_TO_ALCHEMY}\\imgs\\sharp_scroll.png', threshold=0.75, func=1)

        if scroll_cords:
            x = scroll_cords[0] + 1400
            y = scroll_cords[1] + 280
            print(scroll_cords)

            ahk.mouse_actions('move', x=x, y=y)
            for i in range(2):
                ahk.mouse_actions('click')
        else:
            self._craft_sharp_scrolls()
            return False
    def _put_items_in_sharp_scrol(self, amount, is_2_sharp=False):
        time.sleep(1.5)
        ahk.mouse_actions('move', x=1705, y=815)
        ahk.mouse_actions('click')

        time.sleep(1.5)
        ahk.mouse_actions('move', x=1450, y=285)
        ahk.mouse_actions('click')

        time.sleep(1.5)
        ahk.mouse_actions('move', x=1600, y=820)
        ahk.mouse_actions('click')

        time.sleep(0.3)

        equiped_items = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_equiped.png', f'{PATH_TO_ALCHEMY}\\imgs\\item_equiped_in_sharp_menu.png',
                                       need_for_taking_screenshot=True, threshold=0.8, area_of_screenshot=(550, 375, 1300, 570), func=1)
        while equiped_items:
                ahk.mouse_actions('move', x=600+equiped_items[0], y=400+equiped_items[1])
                ahk.mouse_actions('click')
                time.sleep(0.3)
                equiped_items = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_equiped.png', f'{PATH_TO_ALCHEMY}\\imgs\\item_equiped_in_sharp_menu.png',
                               need_for_taking_screenshot=True, threshold=0.8, area_of_screenshot=(550, 375, 1300, 570), func=1)

        red_items = False
        while red_items is False:
            red_items = self.take_off_red_items_from_sharp_menu()

        if not self._check_if_not_enough_scrolls_for_sharp():
            print('Недостаточно свитков для заточки бижи')
            self._craft_sharp_scrolls()
            return False
        ahk.mouse_actions('move', x=950, y=800)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1100, y=700)
        ahk.mouse_actions('click')

        time.sleep(4)

        if is_2_sharp:
            ahk.mouse_actions('move', x=670, y=680)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=950, y=800)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=1100, y=700)
            ahk.mouse_actions('click')

        time.sleep(4)

        if self.check_if_items_got_sharp(amount) is False:
            self._close_sharp_menu()
            return False
        self._exit_from_sharp_scroll()

        self._close_sharp_menu()

    def _check_if_not_enough_scrolls_for_sharp(self):
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_enough_scrolls_for_sharp.png', area_of_screenshot=(750, 780, 752, 782))
        color_of_button = image.get_main_color(f'{PATH_TO_ALCHEMY}\\imgs\\is_enough_scrolls_for_sharp.png')

        if 200 <= color_of_button[0] <= 230 and 95 <= color_of_button[1] <= 115 and 5 <= color_of_button[2] <= 20:
            return True
        return False

    def take_off_red_items_from_sharp_menu(self):
        y_cords = 460
        for i in range(8):
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png', area_of_screenshot=(572+(i*93), y_cords, 574+(i*93), y_cords+1))
            if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png') is True:
                print(f'Обнаружена красная шмотка в {i} слоте 1ый ряд')
                ahk.mouse_actions('move', x=575+(i*95), y=y_cords)
                ahk.mouse_actions('click')
                return False
        y_cords = 560
        for i in range(8):
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png', area_of_screenshot=(572+(i*93), y_cords, 574+(i*93), y_cords+1))
            if self._check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png') is True:
                print(f'Обнаружена красная шмотка в {i} слоте 1ый ряд')
                ahk.mouse_actions('move', x=575+(i*95), y=y_cords-15)
                ahk.mouse_actions('click')
                return False
        print('Красных шмоток не найдено')
        return True

    def check_if_items_got_sharp(self, amount):
        addictional_cord_x = 0
        for i in range(amount):
            if i > 0:
                addictional_cord_x = 10

            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_slot_sharp.png', area_of_screenshot=(560+(i*100)-addictional_cord_x, 385,
                                                                                                 655+(i*100)-addictional_cord_x, 475))

            if image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_slot_sharp.png', f'{PATH_TO_ALCHEMY}\\imgs\\empty_sharp_slot.png', threshold=0.7) is True:
                return False
        return True

    def _craft_sharp_scrolls(self):
        ahk.mouse_actions('move', x=930, y=320)

        ahk.mouse_actions('press')

        while image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_scroll_craft_button_found.png',
                             f'{PATH_TO_ALCHEMY}\\imgs\\sharp_scroll_craft_button.png',
                              need_for_taking_screenshot=True, area_of_screenshot=(1390, 595, 1580, 660)) is False:
            ahk.mouse_actions('move', x=1700, y=450)
            ahk.mouse_actions('drag', x=0, y=-100)
            time.sleep(1)

        ahk.mouse_actions('move', x=1500, y=630)
        ahk.mouse_actions('click')

        time.sleep(2)

        ahk.mouse_actions('move', x=1070, y=960)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1540, y=950)
        ahk.mouse_actions('click')

        time.sleep(5)

        for _ in range(5):
            ahk.mouse_actions('move', x=770, y=950)
            ahk.mouse_actions('click')
            time.sleep(0.1)

        ahk.mouse_actions('esc')

    def _make_roll_for_40_50_roll(self, forecast_colors, roll, need_check_symbol, need_find_by_image, list_of_appropriate_roll_items, slots):
        is_roll_done = False
        while is_roll_done is False:
            is_color_good = False
            while not is_color_good:
                self._repeat_forecast()
                time.sleep(0.6)
                color_true, color_of_forecast = self.check_neccesary_color_of_forecast(forecast_colors)
                if color_true is True:
                    forecast_not_opened_counter = 0
                    while not image.is_forecast_opened():
                        forecast_not_opened_counter += 1
                        self._open_forecast()
                        if forecast_not_opened_counter >= 50:
                            self._go_to_alchemy()
                            forecast_not_opened_counter = 0
                    if self.is_diamonds_in_forecast():
                        ahk.mouse_actions('esc')
                    else:
                        print('Ролл без кристалов на нужном свечении создан')
                        is_color_good = True
                else:
                    continue
            if self.check_items_price(slots, list_of_appropriate_roll_items, red_check=False,
                                      need_for_totaling_prices=False, need_check_sql=False, hwnd=None,
                                      color_of_forecast=color_of_forecast, is_888=False, is_80=False,
                                      need_sequence_matching=True, need_find_by_image=need_find_by_image,
                                      roll=roll, need_check_symbol=need_check_symbol) is False:
                ahk.mouse_actions('esc')
                continue
            else:
                time.sleep(0.2)
                ahk.mouse_actions('esc')
                print('Ролл найден')
                is_roll_done = True

    def _go_to_alchemy(self):
        time.sleep(3)

        while image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_menu_opened.png',
                             f'{PATH_TO_ALCHEMY}\\imgs\\menu_opened.png',
                              need_for_taking_screenshot=True, area_of_screenshot=(1745, 55, 1800, 110)) is False:
            ahk.mouse_actions('move', x=1775, y=85)
            ahk.mouse_actions('click')
            time.sleep(1)

        ahk.mouse_actions('move', x=1425, y=340)
        ahk.mouse_actions('click')
        time.sleep(2)
    def get_window_name(self, hwnd):
        acc_name = win32gui.GetWindowText(hwnd)
        acc_name = acc_name.replace('Lineage2M l ', '')
        return acc_name

    def _wheel_inventory_down(self):
        for i in range(17):
            ahk.mouse_actions('wheel')

    def make_new_price(self, price):
        price = str(price)
        price_is_correct = False
        while price_is_correct is False:
            for i in price:
                if i == '1':
                    ahk.mouse_actions('move', x=1055, y=835)
                    ahk.mouse_actions('click')
                if i == '2':
                    ahk.mouse_actions('move', x=1140, y=835)
                    ahk.mouse_actions('click')
                if i == '3':
                    ahk.mouse_actions('move', x=1220, y=835)
                    ahk.mouse_actions('click')
                if i == '4':
                    ahk.mouse_actions('move', x=1055, y=775)
                    ahk.mouse_actions('click')
                if i == '5':
                    ahk.mouse_actions('move', x=1140, y=775)
                    ahk.mouse_actions('click')
                if i == '6':
                    ahk.mouse_actions('move', x=1220, y=775)
                    ahk.mouse_actions('click')
                if i == '7':
                    ahk.mouse_actions('move', x=1055, y=720)
                    ahk.mouse_actions('click')
                if i == '8':
                    ahk.mouse_actions('move', x=1140, y=720)
                    ahk.mouse_actions('click')
                if i == '9':
                    ahk.mouse_actions('move', x=1220, y=720)
                    ahk.mouse_actions('click')
                if i == '0':
                    ahk.mouse_actions('move', x=1300, y=835)
                    ahk.mouse_actions('click')

            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\seted_price.png', area_of_screenshot=(1085, 630, 1270, 680))
            image.clear_number_for_detect_seted_price(f'{PATH_TO_ALCHEMY}\\imgs\\seted_price.png')
            seted_price = pytesseract.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\seted_price.png', config='--psm 7 -c tessedit_char_whitelist=0123456789')
            print('Цена которую выставил ', seted_price)
            print('Цена которую должен выставить', price)
            if str(seted_price).replace(' ', '').replace('\n', '') == str(price).replace(' ', '').replace('\n', ''):
                price_is_correct = True
            else:
                print('Цена выставлена неправильно!!!')
                for i in range(9):
                    ahk.mouse_actions('move', x=1300, y=720)
                    ahk.mouse_actions('click')
        print('Цена выставлена')

    def confirm_new_price(self):
        ahk.mouse_actions('move', x=1100, y=925)
        ahk.mouse_actions('click')
        time.sleep(0.7)

        ahk.mouse_actions('move', x=1050, y=760)
        ahk.mouse_actions('click')
        time.sleep(0.7)

    def _close_market(self):
        ahk.mouse_actions('move', x=1800, y=90)
        ahk.mouse_actions('click')


roll = Rolls()

class Roll_00():
    def __init__(self, colors=(roll.BLUE, roll.WHITE), items_list=None):
        self.colors = colors
        self.items_to_choose = {roll.BLUE: 2, roll.GREEN: 1}
        self.need_except_accessories = True
        self.need_except_sharp = True
        self.slots = [1]
        self.totaling_prices = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\rol_00_items.txt'
        self.red_check = False
        self.need_for_check_roll_items_name = True
        self.need_for_check_sql = True
        self.need_sequence_matching = False
        self.need_find_by_image = False
        self.roll = '00'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time


class Roll_000():
    def __init__(self, colors=(roll.BLUE, roll.WHITE)):
        self.colors = colors
        self.items_to_choose = {roll.BLUE: 3}
        self.need_except_accessories = True
        self.need_except_sharp = True
        self.slots = [2, 1]
        self.totaling_prices = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_000_items.txt'
        self.red_check = False
        self.need_for_check_roll_items_name = True
        self.need_for_check_sql = True
        self.need_sequence_matching = False
        self.need_find_by_image = False
        self.roll = '000'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time


class Roll_66():
    def __init__(self, colors=(roll.GOLD)):
        global MINIMAL_PRICE_FOR_ROLL
        MINIMAL_PRICE_FOR_ROLL = 0
        self.colors = colors
        self.items_to_choose = {roll.PLUS_1_ACCESORY: 2, roll.BLUE: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3]
        self.totaling_prices = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\rol_66_items.txt'
        self.red_check = True
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '66'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories,self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,
                                                                                                                                                        accesory_items_list=accesory_items_list, need_find_by_image=self.need_find_by_image, roll=self.roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_66_Lite():
    def __init__(self, colors=(roll.GOLD, roll.BLUE)):
        self.colors = colors
        self.items_to_choose = {roll.PLUS_1_ACCESORY: 2, roll.BLUE: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3]
        self.totaling_prices = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\rol_66_items.txt'
        self.red_check = True
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '66'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories,self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,
                                                                                                                                                        accesory_items_list=accesory_items_list, need_find_by_image=self.need_find_by_image, roll=self.roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_32():
    def __init__(self, colors=(roll.BLUE, roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PLUS_3_ACCESORY: 1,
                                roll.PLUS_2_ACCESORY: 1,
                                roll.BLUE: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [2]
        self.totaling_prices = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\rol_66_items.txt'
        self.red_check = False
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '32'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_80():
    def __init__(self, colors=(roll.BLUE, roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PIECE: 1, roll.BLUE: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3]
        self.totaling_prices = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_80_888_items.txt'
        self.red_check = True
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_80 = True
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '80'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_80=True)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_888():
    def __init__(self, colors=(roll.BLUE, roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PIECE: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3]
        self.totaling_prices = False
        self.red_check = True
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_80_888_items.txt'
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_888 = True
        self.need_sequence_matching = True
    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching)
        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time


class Roll_888_K():
    def __init__(self, colors=(roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.RED: 1, roll.BLUE: 2}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3]
        self.totaling_prices = False
        self.red_check = True
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_80_888_items.txt'
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_888 = True
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '888'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_888=True)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_40():
    def __init__(self, colors=(roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PLUS_4_RED_ACCESORY: 1, roll.RED: 4}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3]
        self.totaling_prices = False
        self.red_check = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_80_888_items.txt'
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_888 = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '40'
        self.need_check_symbol = False
        self.need_to_roll = False

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_888=False, need_check_symbol=self.need_check_symbol, need_to_roll=self.need_to_roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_40_Symbol():
    def __init__(self, colors=(roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PLUS_4_RED_ACCESORY: 1, roll.RED: 4}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3]
        self.totaling_prices = False
        self.red_check = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_40_50_items.txt'
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_888 = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '40'
        self.need_check_symbol = True
        self.need_to_roll = False

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_888=False, need_check_symbol=self.need_check_symbol, need_to_roll=self.need_to_roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_50():
    def __init__(self, colors=(roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PLUS_5_RED_ACCESORY: 1, roll.RED: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [2]
        self.totaling_prices = False
        self.red_check = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_80_888_items.txt'
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_888 = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '50'
        self.need_check_symbol = False
        self.need_to_roll = False

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_888=False, need_check_symbol=self.need_check_symbol, need_to_roll=self.need_to_roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_50_Symbol:
    def __init__(self, colors=(roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PLUS_5_RED_ACCESORY: 1, roll.RED: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [2]
        self.totaling_prices = False
        self.red_check = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_40_50_items.txt'
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_888 = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '50'
        self.need_check_symbol = True
        self.need_to_roll = False

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_888=False, need_check_symbol=self.need_check_symbol, need_to_roll=self.need_to_roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time

class Roll_50_Symbol_Plus:
    def __init__(self, colors=(roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PLUS_5_RED_ACCESORY: 1, roll.RED: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [3, 2]
        self.totaling_prices = False
        self.red_check = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\roll_40_50_items.txt'
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_888 = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '50_plus'
        self.need_check_symbol = True
        self.need_to_roll = False

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_888=False, need_check_symbol=self.need_check_symbol, need_to_roll=self.need_to_roll)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time


class Roll_80_Red:
    def __init__(self, colors=(roll.GOLD)):
        self.colors = colors
        self.items_to_choose = {roll.PIECE: 1, roll.BLUE: 3}
        self.need_except_accessories = False
        self.need_except_sharp = False
        self.slots = [2]
        self.totaling_prices = False
        self.appropriatable_items = f'{PATH_TO_ALCHEMY}\\rol_66_items.txt'
        self.red_check = False
        self.need_for_check_roll_items_name = False
        self.need_for_check_sql = False
        self.is_80 = False
        self.need_sequence_matching = True
        self.need_find_by_image = True
        self.roll = '80red'

    def start_roll(self, items_list, accesory_items_list, roll_amount, hwnd):
        items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item, wasted_time = roll.make_roll(self.colors, self.items_to_choose, self.need_except_accessories, self.need_except_sharp,
                                                                                                                                                        self.slots, self.totaling_prices, self.appropriatable_items, self.red_check, self.need_for_check_roll_items_name, items_list,
                                                                                                                                                        roll_amount, tg=None, hwnd=hwnd, need_check_sql=self.need_for_check_sql, need_sequence_matching=self.need_sequence_matching,accesory_items_list=accesory_items_list,
                                                                                                                                                        need_find_by_image=self.need_find_by_image, roll=self.roll, is_80=False)

        print(items_on_market, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot, gained_item)
        return items_on_market, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, slot+1, gained_item, wasted_time


