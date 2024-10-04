from ahk import AHK
from PIL import Image as pil
from difflib import SequenceMatcher

import psutil

import PIL.ImageGrab
import numpy as np
import cv2
import pytesseract

import win32gui
import win32com.client
import win32con
import gspread
import mysql.connector

import telebot
import requests
import TGNotifier

import datetime
import random
import time
import json


#Сюда вписывать номер листа в котором будет указываться ежедневная стата каждый месяц
NUMBER_OF_SHEET_TO_WRITE_STATS_FOR_DAYS = 10
#Сюда указывать время для работы
TIME_FOR_WORK =('03:56', '', '')
#Номер времени в списке в которое будут меняться цены. Отсчет идет от нуля
MAIN_TIME = 1
#Максимальная разница между текущей ценой и минимальной
MAXIMUM_PERCENTAGE_DIFFERENCE = 15
#Минимальная цена по которой будут выставляться красные шмотки на глобал ауке
GLOBAL_MARKET_MINIMAL_PRICE = 300

PATH_TO_AUTOSELL = r'C:\Users\MIFIKUS\PycharmProjects\BigBot\Autosell\\'

MULTIPLIER = 1

TG_USER_ID = 420909529
TG_API_KEY = '6030586977:AAEPBYOO-za3FoNCdkdVcDvQd63YoD_7PKk'
TG_OVERFLOW_API_KEY = '6782899903:AAEZT3pgxMA_QKXyS6Kzz5jzLCyo9EMV6Bg'

bot = telebot.TeleBot(TG_API_KEY)
overflow_bot = telebot.TeleBot(TG_OVERFLOW_API_KEY)

autohotkey = AHK()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

accounts = []
amount_on_market = []
acounts_cells_for_sheet = []
cells_for_days = {}
server_for_accs = {}

class AHKActions:
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
                except Exception:
                    pass

            return
        elif action == 'click':
            while True:
                try:
                    autohotkey.click(direction='D')
                    time.sleep(0.1)
                    autohotkey.click(direction='U')
                    break
                except Exception:
                    pass
            time.sleep(0.2)
            return

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
            while True:
                try:
                    autohotkey.key_press('esc')
                    break
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
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'AutoHotkey.exe':
                    proc.kill()
        except Exception as e:
            print(e)
            print("AHK process doesn't exists anymore")


class Image():
    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):
        if need_for_taking_screenshot:
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

        for pt in zip(*loc[::-1]):
            return pt
        return False

    def take_screenshot(self, image_name, area_of_screenshot=None):
        if area_of_screenshot:
            PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
        else:
            PIL.ImageGrab.grab().save(image_name)
    def image_to_string(self, image_name, is_digits, fill_diamond=True, denoise=True):
        if denoise:
            self._denoise_image(image_name)
        if fill_diamond is True:
            self.fill_the_diamond_with_black()
        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789/')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 3')
        return text

    def upscale_image(self, image_name):
        image.take_screenshot(image_name, area_of_screenshot=(385, 605, 420, 670))
        src = cv2.imread(image_name, cv2.IMREAD_UNCHANGED)
        scale_percent = 400
        width = int(src.shape[1] * scale_percent / 100)
        height = int(src.shape[0] * scale_percent / 100)
        dsize = (width, height)
        output = cv2.resize(src, dsize)

        cv2.imwrite(image_name, output)

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

    def is_inventory_overflow(self, hwnd):
        acc_name = win32gui.GetWindowText(hwnd)
        if self.matching(f'{PATH_TO_AUTOSELL}is_inventory_overflow.jpg', f'{PATH_TO_AUTOSELL}inventory_is_overlow.png', need_for_taking_screenshot=True, threshold=0.65) is True:
            print("Инвентарь переполнен. Замечен 1ым способом")
            TGNotifier.send_overflow_msg(acc_name)
            return True
        if self.matching(f'{PATH_TO_AUTOSELL}is_inventory_overflow.jpg', f'{PATH_TO_AUTOSELL}inventory_is_overlow_2.png', need_for_taking_screenshot=True, threshold=0.60) is True:
            print("Инвентарь переполнен. Замечен 2ым способом")
            TGNotifier.send_overflow_msg(acc_name)
            return True
        return False

    def fill_the_diamond_with_black(self, file='minimal_price.png'):
        #смотрим минимальную цену, чтобы потом закрасить там кристалик
        img_rgb = cv2.imread(f'{PATH_TO_AUTOSELL}{file}')

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(f'{PATH_TO_AUTOSELL}diamond.png', 0)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (15, 18, 22), -1)

        cv2.imwrite(f'{PATH_TO_AUTOSELL}{file}', img_rgb)

    def fill_the_diamond_on_balance(self, is_global_market=False):
        if is_global_market:
            template_path = f'{PATH_TO_AUTOSELL}income_label_global_market.png'
        else:
            template_path = f'{PATH_TO_AUTOSELL}income_label.png'
        img_rgb = cv2.imread(f'{PATH_TO_AUTOSELL}income.png')

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_path, 0)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w + 3, pt[1] + h + 3), (13, 16, 20), -1)

        cv2.imwrite(f'{PATH_TO_AUTOSELL}income.png', img_rgb)
    def get_main_color(self, file):
        img = pil.open(file)
        colors = img.getcolors(256)  # put a higher value if there are many colors in your image
        max_occurence, most_present = 0, 0
        try:
            for c in colors:
                if c[0] > max_occurence:
                    (max_occurence, most_present) = c
            return most_present
        except TypeError:
            raise Exception("Too many colors in the image")

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

    def clear_image_for_previous_price(self, file):
        im = cv2.imread(file)

        WhiteMin = np.array([60, 70, 70], np.uint8)
        WhiteMax = np.array([255, 255, 255], np.uint8)

        HSV = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(HSV, WhiteMin, WhiteMax)
        inverse_cachement_mask = cv2.bitwise_not(mask)

        im[inverse_cachement_mask>0] = [0, 0, 0]
        cv2.imwrite(file, im)
        #print(pytesseract.image_to_string(file))

    def add_to_good_a_red_dot(self):
        im1 = pil.open(f'{PATH_TO_AUTOSELL}good.png')
        im2 = pil.open(f'{PATH_TO_AUTOSELL}dot.png')

        text_img = pil.new('RGBA', (90,90), (0, 0, 0, 0))
        text_img.paste(im1, (0,0))
        text_img.paste(im2, (75,6), mask=im2)
        text_img.save(f'{PATH_TO_AUTOSELL}good.png', quality=100)

        im1.close()
        im2.close()

    def check_if_there_is_error_after_unlock_window(self):
        self.take_screenshot(f'{PATH_TO_AUTOSELL}is_there_error_button.png', area_of_screenshot=(550, 420, 1250, 800))
        is_there_error = self.matching(f'{PATH_TO_AUTOSELL}is_there_error_button.png',
                                       f'{PATH_TO_AUTOSELL}error_after_unlock_button.png',
                                       need_for_taking_screenshot=False, threshold=0.7)

        if is_there_error:
            ahk.mouse_actions('move', x=950, y=620)
            ahk.mouse_actions('click')
            time.sleep(3)
ahk = AHKActions()
image = Image()

class Windows():
    def switch_windows(self, func, current_time):
        shell = win32com.client.Dispatch("WScript.Shell")

        windows_list = self.__find_windows()

        print('Спиок открытых окок с линейкой', windows_list)

        if len(windows_list) > 0:
            for window in windows_list:
                for i in range(3):
                    shell.SendKeys('%')
                    win32gui.ShowWindow(window, win32con.SW_RESTORE)
                    while True:
                        try:
                            win32gui.SetForegroundWindow(window)
                            break
                        except:
                            pass
                    while self.is_screen_locked() is True:
                        self.unlock_screen()
                        image.check_if_there_is_error_after_unlock_window()
                if self._is_dead() is True:
                    self._revive()
                    time.sleep(5)
                func(window, current_time)

    def _is_dead(self):
        image.take_screenshot(f'{PATH_TO_AUTOSELL}main_screen.jpg')
        if image.matching(f'{PATH_TO_AUTOSELL}main_screen.jpg', f'{PATH_TO_AUTOSELL}dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching(f'{PATH_TO_AUTOSELL}main_screen.jpg', f'{PATH_TO_AUTOSELL}dead2.png', need_for_taking_screenshot=True) is True:
            return True

    def _revive(self):
        def __send_to_last_location():
            ahk.mouse_actions('move', x=350, y=180)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=250, y=340)
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

    def is_screen_locked(self):
        for i in range(2):
            is_locked = image.matching(f'{PATH_TO_AUTOSELL}main_screen.jpg', f'{PATH_TO_AUTOSELL}screen_is_locked.png', need_for_taking_screenshot=True)
        return is_locked

    def unlock_screen(self):
        ahk.mouse_actions('move', x=960, y=540)
        ahk.mouse_actions('drag', x=100, y=100)

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

    def update_statistics(self, acc_name):
        ahk.mouse_actions('move', x=1775, y=85)
        ahk.mouse_actions('click')
        time.sleep(0.5)

        ahk.mouse_actions('move', x=1510, y=470)
        ahk.mouse_actions('click')
        time.sleep(0.5)

        ahk.mouse_actions('move', x=700, y=185)
        ahk.mouse_actions('click')
        time.sleep(0.5)

        image.take_screenshot(f'{PATH_TO_AUTOSELL}sold_items.png', area_of_screenshot=(160, 960, 245, 1000))
        image.take_screenshot(f'{PATH_TO_AUTOSELL}income.png', area_of_screenshot=(1050, 950, 1525, 1030))

        database.delete_sold_item_drom_db(acc_name)
        database.get_prices_and_item_names()

        ahk.mouse_actions('move', x=1550, y=980)
        ahk.mouse_actions('click')
        time.sleep(0.5)

        ahk.mouse_actions('move', x=400, y=190)
        ahk.mouse_actions('click')
        time.sleep(0.5)
        image.take_screenshot(f'{PATH_TO_AUTOSELL}balance.png', area_of_screenshot=(730, 65, 908, 100))
        image.take_screenshot(f'{PATH_TO_AUTOSELL}slots.png', area_of_screenshot=(150, 930, 235, 980))
        image.take_screenshot(f'{PATH_TO_AUTOSELL}balance_on_market.png', area_of_screenshot=(385, 935, 520, 985))

        time.sleep(0.5)
        image.fill_the_diamond_on_balance()
        balance = pytesseract.image_to_string(f'{PATH_TO_AUTOSELL}balance.png', config='--psm 11 -c tessedit_char_whitelist=0123456789')
        income = pytesseract.image_to_string(f'{PATH_TO_AUTOSELL}income.png', config='--psm 11 -c tessedit_char_whitelist=0123456789')
        slots = image.image_to_string(f'{PATH_TO_AUTOSELL}slots.png', is_digits=True).replace('\n', '').split('/')
        balance_on_market = pytesseract.image_to_string(f'{PATH_TO_AUTOSELL}balance_on_market.png', config='--psm 11 -c tessedit_char_whitelist=0123456789')

        try:
            slots = int(slots[1]) - int(slots[0])
        except:
            pass
        ahk.mouse_actions('esc')

        return acc_name, balance_on_market, balance, income, slots

class GoogleSheets():
    def write_google(self, nick, market_balance, main_balance, sold_balance, slots):
        SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1qwPa93plt7a_ArFfi05tQZ3pl5o1BSfcIet9GtePkFo/edit#gid=0"
        gs = gspread.service_account('credential_for_statistics.json')
        sh = gs.open_by_url(SPREADSHEET_URL)
        cell = self.get_cell_for_nick(nick)
        try:
            try:
                day = datetime.datetime.now().day

                cell_for_day = cells_for_days.get(str(day))
                print(cell)
                print(cell_for_day)
                sold_balance = int(sh.get_worksheet(NUMBER_OF_SHEET_TO_WRITE_STATS_FOR_DAYS-1).get(f'{cell_for_day}{cell}')[0][0]) + int(sold_balance)
            except:
                sold_balance = 0 + int(sold_balance)

            sh.get_worksheet(NUMBER_OF_SHEET_TO_WRITE_STATS_FOR_DAYS-1).update(f'{cell_for_day}{cell}', sold_balance)
            sh.sheet1.update(f'A{cell}', int(market_balance))
            sh.sheet1.update(f'B{cell}', int(main_balance))
            sh.sheet1.update(f'E{cell}', int(slots))

        except Exception as e:
            print("LOGGING\n",
                  'Nick ', nick,
                  'Error ', e, '\n',
                  'Place ', 'write_google')

    def write_amount_of_items_that_need_to_be_replaced(self, acc_name, amount_of_items):
        cell = self.get_cell_for_nick(acc_name)
        if cell is None:
            print(f'Аккаунта {acc_name} нет в списке')
            return

        SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1qwPa93plt7a_ArFfi05tQZ3pl5o1BSfcIet9GtePkFo/edit#gid=0"

        gs = gspread.service_account('credential_for_statistics.json')
        sh = gs.open_by_url(SPREADSHEET_URL)
        sh.sheet1.update(f'G{cell}', amount_of_items)

        print(f'На аккаунте {acc_name} обновленно количество шмоток которые нужно переставить. Кол-во {amount_of_items}')

    def get_cell_for_nick(self, nick):
        try:
            nick_in_cell = acounts_cells_for_sheet.get(nick)
            print(nick)
            print(nick_in_cell)
            return nick_in_cell[1::]
        except:
            return None

class Telegram_bot():
    def send_msg_to_tg(self, window, message='', type = '', percents=0, amount=0, previous_price=0, minimal_price=0):
        while True:
            try:
                acc_name = win32gui.GetWindowText(window)
                acc_name = acc_name.replace('Lineage2M l ', '')
                item_name = message.replace('\n', '')

                if type == 'overflow':
                    overflow_bot.send_message(TG_USER_ID, f'На аккаунте {acc_name} переполнен инвентарь (')
                    print("Сообщение в тг отправлено")

                elif type == '>10%':
                    bot.send_message(TG_USER_ID, f'Аккаунт: *{acc_name}*({MAXIMUM_PERCENTAGE_DIFFERENCE}%)\n'
                                                 f'Вещь: *{item_name}*\n'
                                                 f'Прошлая цена: *{previous_price}*💎\n'
                                                 f'Минимальная цена на ауке: *{minimal_price}*💎\n'
                                                 f'Разница: *{amount}*💎({percents}%)',
                                                 parse_mode="Markdown")

                    print("Сообщение в тг отправлено")

                elif type == 'red_low_price':
                    bot.send_message(TG_USER_ID, f'На аккаунте {acc_name} цена на красную шмотку меньше 1000. Бот остановлен')

                elif type == 'red_item_less_minimal_price':
                    bot.send_message(TG_USER_ID, f'Аккаунт: *{acc_name}*({GLOBAL_MARKET_MINIMAL_PRICE})\n'
                                                 f'Вещь: *{item_name}*\n'
                                                 f'Прошлая цена: *{previous_price}*💎\n'
                                                 f'Минимальная цена на ауке: *{minimal_price}*💎\n'
                                                 f'Снято потому что стоит меньше *{GLOBAL_MARKET_MINIMAL_PRICE}*💎',
                                                 parse_mode="Markdown")
                break
            except requests.exceptions.ConnectionError as e:
                print('Не удалось подключить к серверам тг')
                print(e)

image = Image()

class Database:
    def __init__(self):
        self.host = '192.168.0.18'
        #self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'BigBot'
        #self.password = 'root'
    
    def delete_sold_item_drom_db(self, acc_name):
        for i in range(6):
            image.take_screenshot(f'{PATH_TO_AUTOSELL}sold_item.png',area_of_screenshot=(180, 310+(115*i), 720, 345+(115*i)))
            item_name = image.image_to_string(f'{PATH_TO_AUTOSELL}sold_item.png', is_digits=False).replace(' ', '').replace('\n', '').lower()
            item_name = item_name.replace("'", "").replace('"', '')
            self._delete_sold_item_from_db_sql_script(item_name, acc_name)
            print('Попытка удалить ', item_name)

    def _delete_sold_item_from_db_sql_script(self, item_name, acc_name):

        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        connection.autocommit = True
        cursor = connection.cursor()
        server_name = server_for_accs.get(acc_name)
        item_name = item_name.replace('\\', '')

        script = f"DELETE FROM alchemy.gained_items WHERE item_name = '{item_name}' AND server_name = '{server_name}'"

        print('server:', server_name)
        print('item_name:', item_name)
        print('acc_name:', acc_name)
        print('script:', script)

        cursor.execute(script)
        cursor.close()

    def get_prices_from_db(self, item_name) -> dict or bool:
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        connection.autocommit = True
        cursor = connection.cursor()

        script = f"SELECT price FROM autosell.items WHERE item_name = '{item_name}'"

        cursor.execute(script)
        result = cursor.fetchall()
        cursor.close()
        if len(result) == 0:
            return False

        price_list = []
        for i in result:
            for j in i:
                price_list.append(j)

        return {'min_price': min(price_list), 'max_price': max(price_list)}

    def add_item_to_db(self, item_name: str, price: int):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        connection.autocommit = True
        cursor = connection.cursor()

        query = f'''
                INSERT INTO autosell.items(item_name, price)
                VALUES ("{item_name}" , {price})
            '''

        cursor.execute(query)
        cursor.close()

    def get_prices_and_item_names(self) -> dict or bool:
        def _collect_prices():
            prices_list = []
            for i in range(6):
                image.take_screenshot(f'{PATH_TO_AUTOSELL}sold_price.png', area_of_screenshot=(790, 320+(115*i), 950, 360+(115*i)))
                price = image.image_to_string(f'{PATH_TO_AUTOSELL}sold_price.png', True)
                try:
                    prices_list.append(int(price))
                except Exception:
                    prices_list.append(False)
            return prices_list

        def _collect_item_names():
            item_names_list = []
            for i in range(6):
                image.take_screenshot(f'{PATH_TO_AUTOSELL}sold_item.png',
                                      area_of_screenshot=(180, 310 + (115 * i), 720, 345 + (115 * i)))
                item_name = image.image_to_string(f'{PATH_TO_AUTOSELL}sold_item.png', is_digits=False).replace(' ', '').replace('\n', '').lower()
                item_name = item_name.replace("'", "").replace('"', '')

                item_names_list.append(item_name)

            return item_names_list

        prices = _collect_prices()
        item_names = _collect_item_names()

        for item_name, price in zip(item_names, prices):
            print(f'Попытка обработать {item_name} с ценой {price}')
            if price is False:
                print('Не удалось получить цену')
                continue

            try:
                print('Попытка загрузить в бд информацию')
                self.add_item_to_db(item_name, price)
            except Exception as e:
                print(f'Не удалось загрузить инфу в БД {e}')

windows = Windows()

ahk = AHKActions()
telegram = Telegram_bot()
database = Database()

class InGame():
    def go_to_menu(self):
        image.take_screenshot('Autosell\\is_menu_opened.png', (1730, 180, 1820, 292))
        while not image.matching('Autosell\\is_menu_opened.png', 'menu_opened.png'):
            ahk.mouse_actions('move', x=1780, y=75)
            ahk.mouse_actions('click')
            time.sleep(0.5)
            image.take_screenshot('Autosell\\is_menu_opened.png', (1730, 180, 1820, 292))


    def go_to_market(self):
        image.take_screenshot(f'{PATH_TO_AUTOSELL}is_market_opened.png', (1560, 70, 1745, 120))

        while image.matching(f'{PATH_TO_AUTOSELL}is_market_opened.png', f'{PATH_TO_AUTOSELL}market_opened.png') is False:
            ahk.mouse_actions('move', x=1500, y=450)
            ahk.mouse_actions('click')
            time.sleep(2)

            image.take_screenshot(f'{PATH_TO_AUTOSELL}is_market_opened.png', (1560, 70, 1745, 120))

    def go_to_global_market(self):
        image.take_screenshot(f'{PATH_TO_AUTOSELL}is_market_opened.png', (1560, 70, 1745, 120))

        while image.matching(f'{PATH_TO_AUTOSELL}is_market_opened.png',
                             f'{PATH_TO_AUTOSELL}market_opened.png') is False:
            ahk.mouse_actions('move', x=1500, y=450)
            ahk.mouse_actions('click')
            time.sleep(2)

            image.take_screenshot(f'{PATH_TO_AUTOSELL}is_market_opened.png', (1560, 70, 1745, 120))

        ahk.mouse_actions('move', x=1450, y=90)
        ahk.mouse_actions('click')

    def go_to_server_settings(self):
        self.go_to_menu()

        ahk.mouse_actions('move', x=1690, y=820)
        ahk.mouse_actions('click')

        time.sleep(4)

        ahk.mouse_actions('move', x=1600, y=180)
        ahk.mouse_actions('click')

    def collect_diamonds_from_global_market(self):
        ahk.mouse_actions('move', x=700, y=185)
        ahk.mouse_actions('click')
        time.sleep(2)

        image.take_screenshot(f'{PATH_TO_AUTOSELL}income.png', area_of_screenshot=(1050, 960, 1520, 1020))
        image.fill_the_diamond_on_balance(is_global_market=True)
        try:
            income = int(image.image_to_string(f'{PATH_TO_AUTOSELL}income.png', is_digits=True))
        except Exception as e:
            print(f'Не удалось получить доход с глобал маркета (collect_diamonds_from_global_market)\n'
                  f'Ошибка: {e}')
            income = 0

        ahk.mouse_actions('move', x=1550, y=980)
        ahk.mouse_actions('click')

        return income

    def go_to_sell_menu(self):
        ahk.mouse_actions('move', x=400, y=200)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('move', x=700, y=200)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('move', x=400, y=200)
        ahk.mouse_actions('click')
        time.sleep(1)

    def go_to_autofit_menu(self):
        ahk.mouse_actions('move', x=1690, y=820)
        ahk.mouse_actions('click')
        time.sleep(4)
        ahk.mouse_actions('move', x=200, y=400)
        ahk.mouse_actions('click')

    def turn_off_autofit(self):
        ahk.mouse_actions('move', x=1700, y=300)
        ahk.mouse_actions('click')

        for i in range(2):
            ahk.mouse_actions('move', x=1700, y=500)
            ahk.mouse_actions('click')

        ahk.mouse_actions('esc')

    def turn_on_autofit(self):
        ahk.mouse_actions('move', x=1200, y=360)
        ahk.mouse_actions('click')

        for i in range(2):
            ahk.mouse_actions('move', x=1500, y=500)
            ahk.mouse_actions('click')

        ahk.mouse_actions('esc')

    def sort_inventory(self):
        ahk.mouse_actions('i')
        time.sleep(0.5)

        ahk.mouse_actions('move', x=1660, y=820)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1660, y=520)
        ahk.mouse_actions('click')

        ahk.mouse_actions('i')

    def take_off_good_from_shop(self, hwnd, is_global):
        if is_global:
            allready_selling_image = f'{PATH_TO_AUTOSELL}global_market_already_selling.png'
        else:
            allready_selling_image = f'{PATH_TO_AUTOSELL}already_selling_good.jpg'
        if is_global:
            for i in range(4):
                if image.matching(f'{PATH_TO_AUTOSELL}shop.jpg', allready_selling_image, need_for_taking_screenshot=True, area_of_screenshot=(1190, 300, 1333, 340), threshold=0.65) is True:
                    print('Все шмотки выставлены!')
                    return True
                time.sleep(1)
        else:
            if image.matching(f'{PATH_TO_AUTOSELL}shop.jpg', allready_selling_image, need_for_taking_screenshot=True, area_of_screenshot=(1190, 300, 1333, 340), threshold=0.65) is True:
                print('Все шмотки выставлены!')
                return True
        #Сохраням скрин шмотки
        image.take_screenshot(f'{PATH_TO_AUTOSELL}good.png', area_of_screenshot=(116, 295, 210, 395))
        image.add_to_good_a_red_dot()
        image.take_screenshot(f'{PATH_TO_AUTOSELL}is_red.jpg', area_of_screenshot=(116, 330, 125, 350))
        cords_for_previous_price = (1011, 325, 1150, 365)

        #Сохраняем скрин прошлой цены шмотки
        time.sleep(1)
        image.take_screenshot(f'{PATH_TO_AUTOSELL}previous_price.png', area_of_screenshot=cords_for_previous_price)
        image.clear_image_for_previous_price(f'{PATH_TO_AUTOSELL}previous_price.png')

        try:
            int(self._get_previous_price_in_string())
        except:
            return False

        image.take_screenshot(f'{PATH_TO_AUTOSELL}item_taked_off.png',area_of_screenshot=(560, 350, 1300, 660))
        while image.matching(f'{PATH_TO_AUTOSELL}is_item_taken_off.png', f'{PATH_TO_AUTOSELL}item_taked_off.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(560, 350, 1300, 660), threshold=0.8) is True:

            ahk.mouse_actions('move', x=1250, y=360)
            ahk.mouse_actions('click')
            time.sleep(0.7)


        image.take_screenshot(f'{PATH_TO_AUTOSELL}item_taked_off.png',area_of_screenshot=(560, 350, 1300, 660))
        while image.matching(f'{PATH_TO_AUTOSELL}is_item_taken_off.png', f'{PATH_TO_AUTOSELL}item_taked_off.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(560, 350, 1300, 660), threshold=0.8) is True:

            ahk.mouse_actions('move', x=1050, y=750)
            ahk.mouse_actions('click')
            time.sleep(0.7)

        if image.is_inventory_overflow(hwnd) is True:
            telegram.send_msg_to_tg(hwnd, type='overflow')
            return True

    def find_good_in_inventory(self):
        def __find_locked_item():
            image.take_screenshot(f'{PATH_TO_AUTOSELL}sell_screen.png', area_of_screenshot=(1380, 320,
                                                                                            1810, 900))
            cords = image.matching(f'{PATH_TO_AUTOSELL}item_is_locked.png', f'{PATH_TO_AUTOSELL}sell_screen.png', threshold=0.8,
                               func=1)
            if cords:
                return cords
            else:
                return False

        image.take_screenshot(f'{PATH_TO_AUTOSELL}sell_screen.png', area_of_screenshot=(1380, 320,
                                               1810, 900))
        cords = image.matching(f'{PATH_TO_AUTOSELL}item_is_equiped.png', f'{PATH_TO_AUTOSELL}sell_screen.png', threshold=0.85,
                                   func=1)
        if cords:
            return cords
        return False

    def wheel_inventory_down(self):
        for i in range(17):
            ahk.mouse_actions('wheel')

    def wheel_inventory_up(self):
        for i in range(17):
            ahk.mouse_actions('wheel_up')

    def sale_good(self, x, y):
        image.take_screenshot(f'{PATH_TO_AUTOSELL}item_taked_off.png',area_of_screenshot=(560, 350, 1300, 660))
        while image.matching(f'{PATH_TO_AUTOSELL}is_item_taken_off.png', f'{PATH_TO_AUTOSELL}item_taked_off.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(560, 350, 1300, 660), threshold=0.75) is True:
            ahk.mouse_actions('move', x=1400 + x, y=340 + y)
            ahk.mouse_actions('click')
            time.sleep(0.7)

    def get_minimal_price(self):
        image.take_screenshot(f'{PATH_TO_AUTOSELL}minimal_price.png', area_of_screenshot=(1220, 459, 1360, 495))

    def _get_previous_price_in_string(self):
        previous_price = image.image_to_string(f'{PATH_TO_AUTOSELL}previous_price.png', is_digits=True,
                                               fill_diamond=False, denoise=False).replace('\n', '').replace(' ', '')
        return previous_price

    def _get_minimal_price_in_string(self):
        minimal_price = image.image_to_string(f'{PATH_TO_AUTOSELL}minimal_price.png', is_digits=True)
        return minimal_price

    def comparison_previous_price_and_minimal_price(self, hwnd, time_for_work, is_global_market):
        def _is_item_in_list(item_name):
            def _prepare_item_name(item_name):
                item_name = item_name.replace(' ', '').replace('\n', '').lower()
                return item_name

            with open(f'{PATH_TO_AUTOSELL}\\items_price_list.json', encoding='utf-8') as file:
                items_price_list = json.load(file)

            item_name = _prepare_item_name(item_name)

            for i in items_price_list.items():
                dict_item_name = _prepare_item_name(i[0])
                if SequenceMatcher(a=dict_item_name, b=item_name).ratio() > 0.95:
                    print(f'{item_name} in roll_00 list')
                    return True
            return False

        image.take_screenshot(f'{PATH_TO_AUTOSELL}item_name.png', area_of_screenshot=(600, 170, 1320, 200))
        item_name = image.image_to_string(image_name=f'{PATH_TO_AUTOSELL}item_name.png', is_digits=False)

        print('comparison_previous_price_and_minimal_price')
        is_item_dumped = True

        previous_price = int(self._get_previous_price_in_string().replace(' ', '').replace('\n', ''))
        print('Прошлая цена ', previous_price)

        if image.get_main_color(f'{PATH_TO_AUTOSELL}is_red.jpg') == (183, 60, 63):
            if previous_price < 1000:
                telegram.send_msg_to_tg(hwnd, type='red_low_price')
                return False
        try:
            minimal_price = int((self._get_minimal_price_in_string()))
        except:
            print('Не удалось получить минимальную цену')
            return previous_price, False, item_name

        diference_in_procensts = abs(minimal_price - previous_price) / previous_price * 100.0

        if is_global_market is True:
            percantage_difference = 5

        elif _is_item_in_list(item_name):
            percantage_difference = 999999999

        else:
            percantage_difference = MAXIMUM_PERCENTAGE_DIFFERENCE

        if diference_in_procensts > percantage_difference:
            telegram.send_msg_to_tg(hwnd, item_name, type='>10%', percents=int(diference_in_procensts),
                                    amount=abs(previous_price-minimal_price), previous_price=previous_price, minimal_price=minimal_price)

            if is_global_market:
                if previous_price <= GLOBAL_MARKET_MINIMAL_PRICE:
                    telegram.send_msg_to_tg(hwnd, item_name, type='red_item_less_minimal_price', percents=int(diference_in_procensts),
                                            amount=abs(previous_price-minimal_price), previous_price=previous_price, minimal_price=minimal_price)
                    return False

            if (time_for_work == TIME_FOR_WORK[MAIN_TIME]) and (previous_price != 10):
                return previous_price - 1, is_item_dumped, item_name
            return previous_price, is_item_dumped, item_name

        if is_global_market:
            if minimal_price <= GLOBAL_MARKET_MINIMAL_PRICE:
                telegram.send_msg_to_tg(hwnd, item_name, type='red_item_less_minimal_price', percents=int(diference_in_procensts),
                                        amount=abs(previous_price-minimal_price), previous_price=previous_price, minimal_price=minimal_price)
                global cords
                cords = self.find_good_in_inventory()
                return False
        if minimal_price == 10:
            return minimal_price, False, item_name
        return minimal_price - 1, False, item_name

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

            image.take_screenshot(f'{PATH_TO_AUTOSELL}seted_price.png', area_of_screenshot=(1085, 630, 1270, 680))
            image.clear_number_for_detect_seted_price(f'{PATH_TO_AUTOSELL}seted_price.png')
            seted_price = pytesseract.image_to_string(f'{PATH_TO_AUTOSELL}seted_price.png', config='--psm 7 -c tessedit_char_whitelist=0123456789')
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
        image.take_screenshot(f'{PATH_TO_AUTOSELL}item_taked_off.png',area_of_screenshot=(560, 350, 1300, 660))
        while image.matching(f'{PATH_TO_AUTOSELL}is_item_taken_off.png', f'{PATH_TO_AUTOSELL}item_taked_off.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(560, 350, 1300, 660), threshold=0.75) is True:
            ahk.mouse_actions('move', x=1100, y=925)
            ahk.mouse_actions('click')
            time.sleep(0.7)

        image.take_screenshot(f'{PATH_TO_AUTOSELL}item_taked_off.png',area_of_screenshot=(560, 350, 1300, 660))
        while image.matching(f'{PATH_TO_AUTOSELL}is_item_taken_off.png', f'{PATH_TO_AUTOSELL}item_taked_off.png', need_for_taking_screenshot=True,
                             area_of_screenshot=(560, 350, 1300, 660), threshold=0.75) is True:
            ahk.mouse_actions('move', x=1050, y=760)
            ahk.mouse_actions('click')
            time.sleep(0.7)

    def get_min_and_max_prices(self, item_name):
        def _prepare_item_name(item_name):
            item_name = item_name.replace(' ', '').replace('\n', '').lower()
            return item_name

        print('item name is', item_name)

        with open(f'{PATH_TO_AUTOSELL}\\items_price_list.json', encoding='utf-8') as file:
            items_price_list = json.load(file)

        item_name = _prepare_item_name(item_name)

        item_found_in_list = False

        for i in items_price_list.items():
            dict_item_name = _prepare_item_name(i[0])
            if SequenceMatcher(a=dict_item_name, b=item_name).ratio() > 0.95:
                min_and_max_prices = i[1]
                item_found_in_list = True
                print(f'{item_name} in roll_00 list')
                break

        if not item_found_in_list:
            print(f'{item_name} NOT in roll_00 list')
            print(f'Попытка получить в базе данных цены для {item_name}')

            min_and_max_prices = database.get_prices_from_db(item_name)
            if min_and_max_prices is False:
                print('Не получилось получить шмотку из базы данных')
                return False

            print('Удалось получить шмотку из базы данных')

        min_price = min_and_max_prices.get('min_price')
        max_price = min_and_max_prices.get('max_price')

        print('min_price', min_price)
        print('max_price', max_price)

        return (min_price, max_price)

windows = Windows()
image = Image()
ahk = AHKActions()
telegram = Telegram_bot()
google = GoogleSheets()
ingame = InGame()
cords = 0
def autosell_global_market(market_balance, sold_balance, hwnd, current_time):
    ingame.go_to_menu()
    ingame.go_to_global_market()
    ingame.go_to_sell_menu()

    while True:
        time.sleep(2)
        image.take_screenshot(f"{PATH_TO_AUTOSELL}are_there_items_on_global_market.png", area_of_screenshot=(100, 295, 220, 400))
        image.take_screenshot(f"{PATH_TO_AUTOSELL}are_there_items_on_global_market_2.png", area_of_screenshot=(230, 610, 1130, 655))
        image.take_screenshot(f"{PATH_TO_AUTOSELL}amount_of_slots_on_global_market.png", area_of_screenshot=(150, 935, 230, 980))

        nothing_on_global_market_text = image.image_to_string(f"{PATH_TO_AUTOSELL}are_there_items_on_global_market_2.png", is_digits=False).replace(' ','').replace('\n', '').lower()
        nothing_on_global_market_text_correct = 'неттоваровнапродажу.откройтесумку,чтобывыбратьпредметы.'
        amount_of_slots_on_global_market = image.image_to_string(f"{PATH_TO_AUTOSELL}amount_of_slots_on_global_market.png", is_digits=True).replace(' ','').replace('\n', '').lower()

        if image.matching(f"{PATH_TO_AUTOSELL}are_there_items_on_global_market.png", f"{PATH_TO_AUTOSELL}nothing_on_global_market.png",
                          threshold=0.65) is True:
            print('На мировом аукционе ничего нет. Понял по области где предмет')
            break
        elif image.matching(f"{PATH_TO_AUTOSELL}are_there_items_on_global_market.png", f"{PATH_TO_AUTOSELL}nothing_on_global_market_1.png",
                            threshold=0.65) is True:
            print('На мировом аукционе ничего нет. Понял по области где предмет')
            break
        elif SequenceMatcher(a=nothing_on_global_market_text, b=nothing_on_global_market_text_correct).ratio() > 0.8:
            print('На мировом аукционе ничего нет.  Понял по надписи в ауке')
            break
        elif amount_of_slots_on_global_market == '0/30':
            print('На мировом аукционе ничего нет.  Понял по колличеству слотов')
            break

        amount_of_wheels_down = 0
        amount_of_wheels_up = 0
        cords_seted = False
        while cords_seted is False:
            cords = ingame.find_good_in_inventory()
            if cords is False:
                print('Не нашел предмет')
                ahk.mouse_actions('move', x=1600, y=600)
                if amount_of_wheels_down < 2:
                    ingame.wheel_inventory_down()
                    amount_of_wheels_down += 1
                    continue
                if amount_of_wheels_up < 2:
                    ahk.mouse_actions('drag', x=0, y=-50)
                else:
                    amount_of_wheels_down = 0
                    amount_of_wheels_up = 0
                    continue
            else:
                cords_seted = True
        if ingame.take_off_good_from_shop(hwnd, True) is True:
            break
        ingame.sale_good(cords[0], cords[1])
        time.sleep(0.5)
        ingame.get_minimal_price()
        try:
            price, is_item_dumped, item_name = ingame.comparison_previous_price_and_minimal_price(hwnd, current_time, True)
        except:
            price = ingame.comparison_previous_price_and_minimal_price(hwnd, current_time, True)
        if price is False:
            ahk.mouse_actions('esc')
            continue
        ingame.make_new_price(price)
        ingame.confirm_new_price()

    image.take_screenshot('balance_on_market.png', area_of_screenshot=(385, 935, 520, 985))
    try:
        balance_on_market = int(image.image_to_string('balance_on_market.png', is_digits=True))
    except:
        balance_on_market = 0

    global_market_sold_balance = ingame.collect_diamonds_from_global_market()
    try:
        income = int(sold_balance) + int(global_market_sold_balance)
    except Exception as e:
        print('Ошибка при получении дохода')
        print(e)
        income = 0

    ahk.mouse_actions('esc')

    return balance_on_market, income

def get_acc_name_by_label():
    for i in range(5):
        image.take_screenshot(f"{PATH_TO_AUTOSELL}acc_name.png", area_of_screenshot=(150, 0, 300, 40))
        acc_name_image = cv2.imread(f"{PATH_TO_AUTOSELL}acc_name.png")

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

    ingame.go_to_server_settings()

    for i in range(5):
        image.take_screenshot(f"{PATH_TO_AUTOSELL}acc_name.png", area_of_screenshot=(1200, 265, 1445, 315))
        acc_name_image = cv2.imread(f"{PATH_TO_AUTOSELL}acc_name.png")

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

def main(hwnd, current_time):
    try:
        acc_name = win32gui.GetWindowText(hwnd)
        acc_name = acc_name.replace('Lineage2M l ', '')

        amount_of_items_to_replace = 0

        if 'Lineage2M' in acc_name:
            print('Не удалось получить название аккаунта по названию окна, переход к следующему способу')
            acc_name = get_acc_name_by_label()
        ingame.go_to_menu()
        ingame.go_to_autofit_menu()
        ingame.turn_off_autofit()

        ingame.sort_inventory()

        ingame.go_to_menu()
        ingame.go_to_market()
        ingame.go_to_sell_menu()

        amount_of_wheels_down = 0
        amount_of_wheels_up = 0
        cords_seted = False
        while cords_seted is False:
            global cords
            cords = ingame.find_good_in_inventory()
            if cords is False:
                print('Не нашел предмет')
                ahk.mouse_actions('move', x=1600, y=600)
                if amount_of_wheels_down < 2:
                    ingame.wheel_inventory_down()
                    amount_of_wheels_down += 1
                    continue
                if amount_of_wheels_up < 2:
                    ingame.wheel_inventory_up()
                    amount_of_wheels_up += 1
                    continue
                else:
                    amount_of_wheels_down = 0
                    amount_of_wheels_up = 0
                    continue
            else:
                cords_seted = True

        while True:
            take_off_goods = ingame.take_off_good_from_shop(hwnd, False)
            is_item_dumped = False

            if take_off_goods is True:
                ahk.mouse_actions('esc')
                break

            if take_off_goods is False:
                ahk.mouse_actions('move', x=850, y=350)
                ahk.mouse_actions('drag', x=0, y=-10)
                continue

            ingame.sale_good(cords[0], cords[1])
            time.sleep(0.5)
            ingame.get_minimal_price()

            price, is_item_dumped, item_name = ingame.comparison_previous_price_and_minimal_price(hwnd, current_time, False)

            if price is False:
                continue

            print('is_item_dumped' , is_item_dumped)
            if is_item_dumped:
                amount_of_items_to_replace += 1
            print('amount_of_items_to_replace', amount_of_items_to_replace)

            #min_and_max_price = ingame.get_min_and_max_prices(item_name)
            #if min_and_max_price:
            #    min_price = min_and_max_price[0]
            #    max_price = min_and_max_price[1]
#
            #    if not min_price < price < max_price:
            #        min_price_diff = abs(price - min_price)
            #        max_price_diff = abs(price - max_price)
#
            #        if min(min_price_diff, max_price_diff) == min_price_diff:
            #            price = min_price
            #        else:
            #            price = max_price
#
            ingame.make_new_price(price)
            ingame.confirm_new_price()

        acc_name, market_balance, main_balance, sold_balance, slots = windows.update_statistics(acc_name)
        global_market_balance, sold_balance = autosell_global_market(market_balance, sold_balance, hwnd, current_time)

        print('Баланс на обычном ауке', market_balance)
        print('Баланс на глобал ауке', global_market_balance)

        if global_market_balance is False:
            print('Нет шмоток на глобал ауке')

        else:
            market_balance = market_balance.replace('\n', '')
            market_balance = market_balance.replace(' ', '')
            try:
                market_balance = int(market_balance)
            except Exception as e:
                print(f'Не удалось получить market balance {e}')
                market_balance = 0
            market_balance += global_market_balance

        ingame.go_to_menu()
        ingame.go_to_autofit_menu()
        ingame.turn_on_autofit()

        windows.lock_screen()

        print('Ник', acc_name)
        print('На ауке', market_balance)
        print('На балансе', main_balance)
        print('Доход', sold_balance)
        print('Слоты', slots)
        print('Нужно переставить шмоток', amount_of_items_to_replace)

        google.write_google(acc_name, market_balance, main_balance, sold_balance, slots)
        google.write_amount_of_items_that_need_to_be_replaced(acc_name, amount_of_items_to_replace)

        del cords
    except Exception as e:
        TGNotifier.send_break_msg('Перестановка', acc_name, e)

def run(schedule, multiplier, path):
    global TIME_FOR_WORK
    global MULTIPLIER
    global PATH_TO_AUTOSELL
    global acounts_cells_for_sheet
    global cells_for_days
    global server_for_accs

    TIME_FOR_WORK = 'Авто'
    MULTIPLIER = int(multiplier)
    print('tuple', TIME_FOR_WORK)
    PATH_TO_AUTOSELL = f'{path}\\Autosell\\'

    with open(f"{PATH_TO_AUTOSELL}acounts_cells_for_sheet.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
        acounts_cells_for_sheet = data
    with open(f"{PATH_TO_AUTOSELL}cells_for_days.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
        cells_for_days = data
    with open(f"{PATH_TO_AUTOSELL}servers_for_accounts.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
        server_for_accs = data

    while True:
        now = time.localtime()
        current_time = time.strftime("%H:%M", now)
        print(current_time)
        if current_time in TIME_FOR_WORK:
            windows.switch_windows(main, current_time)
        elif 'Авто' in TIME_FOR_WORK:
            windows.switch_windows(main, current_time)
            break
        time.sleep(15)