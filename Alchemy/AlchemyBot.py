from ahk import AHK
from PIL import Image as pil

from .rolls import Roll_00, Roll_000, Roll_66, Roll_66_Lite, Roll_32, Roll_80, Roll_80_Red, Roll_888, Roll_888_K, Roll_40, Roll_50, Roll_40_Symbol, Roll_50_Symbol, Roll_50_Symbol_Plus
from .rolls import roll

from Autosell import AutoSellBotFinal
from SborPlushek import script_dlya_sbora_plushek

import pyscreenshot
import numpy as np
import cv2
import pytesseract

import win32gui
import win32com.client
import win32con

import telebot

import random
import datetime
import time

import psutil
import traceback

with open('settings.txt') as f:
    for i in f.readlines():
        if 'path' in i:
            path = i.split('=')[1]
            print(i)
            break

PATH_TO_ALCHEMY = path + '\\Alchemy\\'

MULTIPLIER = 1

TG_USER_ID = 420909529
TG_API_KEY = '6444400617:AAGFcVcsipQrXxrF0J6nzQM_B0RsUDLynPw'
bot = telebot.TeleBot(TG_API_KEY)

autohotkey = AHK()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
accs_and_rolls_dict = {}

with open('alchemy_account_preset.txt', 'r', encoding='windows-1251') as file:
    accs_and_rols = file.read().split('\n')

for i in accs_and_rols:
    try:
        acc_info = i.split(' ')
        acc_name = acc_info[0]
        try:
            colors_of_forecast = []
            colors = acc_info[3]
            colors = colors.split(',')
            for a in colors:
                a = 'roll.' + a
                colors_of_forecast.append(eval(a))
            print(acc_info[1] + f'({colors_of_forecast}).start_roll')
            acc_roll = acc_info[1] + f'({colors_of_forecast}).start_roll'
        except:
            acc_roll = acc_info[1] + '().start_roll'
        amount_of_rols = int(acc_info[2])
        accs_and_rolls_dict[acc_name] = {acc_roll: amount_of_rols}
    except Exception as e:
        print(e)

class AHKActions():

    # Переменная action отвечает за то, какое действие нужно сделать. (кликнуть, перевести мышку, провести мышкой с нажатием)
    @staticmethod
    def mouse_actions(action, x=0, y=0):

        if action == 'move':
            while True:
                if autohotkey.mouse_move(x, y, speed=0) is not False:
                    break

            time.sleep(0.2)
            return
        elif action == 'click':
            while True:
                if autohotkey.click() is not False:
                    break
            time.sleep(0.2)
            return

        elif action == 'drag':
            while True:
                if autohotkey.mouse_drag(x, y, relative=True) is not False:
                    break

            time.sleep(1*MULTIPLIER)
            return

        elif action == 'wheel':
            while True:
                if autohotkey.wheel_down() is not False:
                    break
            return

        elif action == 'esc':
            while True:
                if autohotkey.key_press('esc') is not False:
                    break
            return
        elif action == 'y':
            autohotkey.key_press(y)
            return
        elif action == 'i':
            autohotkey.key_press('i')
            return
        elif action == 'press':
            while True:
                if autohotkey.click(direction='D') is not False:
                    break
            time.sleep(2)
            while True:
                if autohotkey.click(direction='U') is not False:
                    break
            return

        for proc in psutil.process_iter():
            if proc.name() == 'AutoHotkey.exe':
                proc.kill()
class Image():

    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):

        if need_for_taking_screenshot is True:
            if area_of_screenshot:
                main_screen = pyscreenshot.grab(bbox=area_of_screenshot)
            else:
                main_screen = pyscreenshot.grab()
            main_screen.save(main_image_name)

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
            i = pt
        try:
            return pt
        except:
            return False

    def take_screenshot(self, image_name, area_of_screenshot=None):
        if area_of_screenshot:
            main_screen = pyscreenshot.grab(bbox=area_of_screenshot)
        else:
            main_screen = pyscreenshot.grab()
        main_screen.save(image_name)

    def image_to_string(self, image_name, is_digits, fill_diamond=True):
        self._denoise_image(image_name)
        if fill_diamond is True:
            self.fill_the_diamond_with_black()

        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789/')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config=r'--oem 3 --psm 6')
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
        img_rgb = cv2.imread(f'{PATH_TO_ALCHEMY}{file}')

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(f'{PATH_TO_ALCHEMY}diamond.png', 0)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (15, 18, 22), -1)

        cv2.imwrite(f'{PATH_TO_ALCHEMY}{file}', img_rgb)


    def get_main_color(self, file):
        img = pil.open(file)
        colors = img.getcolors(1024)  # put a higher value if there are many colors in your image
        colors = sorted(colors)
        if (0,0,0) in colors:
           colors.remove(colors[0])
        return colors[0][1]


    def get_adena_amount(self) -> int:
        self.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\amount_of_adena.png', (1010, 65, 1180, 100))
        amount_of_adena = self.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\amount_of_adena.png', True, False)

        amount_of_adena = amount_of_adena.replace('\n', '')
        amount_of_adena = amount_of_adena.replace(' ', '')
        amount_of_adena = amount_of_adena.replace('.', '')
        amount_of_adena = amount_of_adena.replace(',', '')

        return int(amount_of_adena)

    def get_diamonds_amount(self) -> int:
        def _delete_diamond_from_img(filename: str):
            img_rgb = cv2.imread(f'{PATH_TO_ALCHEMY}\\imgs\\{filename}')

            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(f'{PATH_TO_ALCHEMY}\\imgs\\balance_diamond.png', 0)

            w, h = template.shape[::-1]

            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

            threshold = 0.7
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (15, 18, 22), -1)

            cv2.imwrite(f'{PATH_TO_ALCHEMY}\\imgs\\{filename}', img_rgb)

        self.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\amount_of_diamonds.png', (800, 65, 910, 100))
        _delete_diamond_from_img('amount_of_diamonds.png')

        amount_of_diamonds = self.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\amount_of_diamonds.png', True, False)

        amount_of_diamonds = amount_of_diamonds.replace(' ', '')
        amount_of_diamonds = amount_of_diamonds.replace('\n', '')
        amount_of_diamonds = amount_of_diamonds.replace('.', '')
        amount_of_diamonds = amount_of_diamonds.replace(',', '')

        return int(amount_of_diamonds)

    def get_amount_of_slots(self) -> int:
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\slots.png', area_of_screenshot=(150, 930, 235, 980))
        return int(image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\slots.png', True, False).replace('\n', '').split('/')[0])

    def get_amount_of_neccesary_scrolls(self) -> int or bool:
        self.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\amount_of_neccessary_scrolls.png', (1060, 710, 1090, 750))
        amount_of_scrolls = self.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\amount_of_neccessary_scrolls.png', True, False)

        amount_of_scrolls = amount_of_scrolls.replace(' ', '')
        amount_of_scrolls = amount_of_scrolls.replace('\n', '')

        print(f'amount_of_scrolls {amount_of_scrolls}')

        try:
            return int(amount_of_scrolls)
        except:
            return False

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

    def is_item_color_blue(self, img):
        try:
            color = image.get_main_color(img)
            print(color)
            if color:
                if (5 <= color[0] <= 35) and (100 <= color[1] <= 130) and (170 <= color[2] <= 256):
                    if image.image_to_string(img, False, False):
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
                    if image.image_to_string(img, False, False):
                        return True
                return False
            else:
                print('Не смог определить красная шмотка или нет. Место: _is_item_color_red')
        except Exception as e:
            print('Error: place: _is_item_color_red\n', e)


ahk = AHKActions()
image = Image()


class Windows:

    def switch_windows(self, func):
        shell = win32com.client.Dispatch("WScript.Shell")

        windows_list = self._get_accs_names()

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

                func(window)
                continue

    def _get_accs_names(self):
        l2m_windows = self.find_windows()
        accs_names_list = []
        for hwnd in l2m_windows:
            acc_name = self.get_window_name(hwnd)
            #if acc_name in accs_and_rolls_dict:
            accs_names_list.append(hwnd)
        return accs_names_list

    def _is_dead(self):
        image.take_screenshot(f'{PATH_TO_ALCHEMY}main_screen.jpg')
        if image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\main_screen.jpg', f'{PATH_TO_ALCHEMY}\\imgs\\dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\main_screen.jpg', f'{PATH_TO_ALCHEMY}\\imgs\\dead2.png', need_for_taking_screenshot=True) is True:
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
        is_locked = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\main_screen.jpg', f'{PATH_TO_ALCHEMY}\\imgs\\screen_is_locked.png',
                                       need_for_taking_screenshot=True, threshold=0.8)
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

    def find_windows(self, window_name='Lineage2M'):

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

    def get_window_name(self, hwnd):
        acc_name = win32gui.GetWindowText(hwnd)
        acc_name = acc_name.replace('Lineage2M l ', '')
        return acc_name

class Telegram:

    def send_msg_in_tg(self, hwnd, type='', adena_wasted=0, roll_type='', amount_of_rolls=0, diamonds_wasted=0, items_bought={}, gained_slot=0, gained_item='', wasted_time=0):
        while True:
            try:
                acc_name = win32gui.GetWindowText(hwnd)
                acc_name = acc_name.replace('Lineage2M l ', '')

                if type == 'overflow':
                    bot.send_message(TG_USER_ID, f'На аккаунте {acc_name} переполнен инвентарь (')
                    print("Сообщение в тг отправлено")

                if type == 'not_found_items':
                    bot.send_message(TG_USER_ID, f'На аккаунте {acc_name} не достаточно шмоток для ролла')

                if type == 'roll info':
                    bought_items_str = ''
                    adena_wasted = '{0:,}'.format(adena_wasted).replace(',', ' ')
                    if len(items_bought) == 0:
                        items_bought == "Ничего не купил\n"
                    else:
                        for i in items_bought.items():
                            item_name = i[0]
                            item_price = i[1]
                            item_str = '*' + item_name + ': ' + str(item_price) + '*' + '\n'
                            bought_items_str += item_str
                    gained_item = gained_item.replace("\n", '')
                    roll_type = roll_type.replace('Roll_', '').replace('().start_roll', '')
                    bot.send_message(TG_USER_ID, f'Аккаунт: *{acc_name}*\n'
                                                 f'Ролл: *{roll_type}\n*'
                                                 f'Потрачено адены: *{adena_wasted}*\n'
                                                 f'Алмазов потрачено: *{diamonds_wasted}*\n'
                                                 f'Купленные шмотки:\n'
                                                 f'{bought_items_str}'
                                                 f'Выпал слот: *{gained_slot}*\n'
                                                 f'Выпала шмотка: *{gained_item}*\n'
                                                 f'Потрачено времени: *{datetime.timedelta(seconds=round(wasted_time))}*',
                                                   parse_mode="Markdown")

                if type == 'end':
                    bot.send_message(TG_USER_ID, f'{acc_name}\n'
                                                 f'Закончил крутить')

            except:
                pass

windows = Windows()


def get_accs_names():
    l2m_windows = windows.find_windows()
    accs_names_list = []
    for hwnd in l2m_windows:
        accs_names_list.append(windows.get_window_name(hwnd))

    return accs_names_list

def sort_inventory():
    ahk.mouse_actions('i')
    time.sleep(1)

    ahk.mouse_actions('move', x=1660, y=820)
    ahk.mouse_actions('click')

    ahk.mouse_actions('move', x=1660, y=520)
    ahk.mouse_actions('click')

    ahk.mouse_actions('esc')

    time.sleep(1)


def sharp_accessory():
    def _check_if_not_enough_scrolls_for_sharp():
        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_enough_scrolls_for_sharp.png', area_of_screenshot=(750, 780, 752, 782))
        color_of_button = image.get_main_color(f'{PATH_TO_ALCHEMY}\\imgs\\is_enough_scrolls_for_sharp.png')

        if 200 <= color_of_button[0] <= 230 and 95 <= color_of_button[1] <= 115 and 5 <= color_of_button[2] <= 20:
            return True
        return False

    def _check_red(image_path):
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

    def take_off_red_items_from_sharp_menu():
        y_cords = 460
        for i in range(8):
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png', area_of_screenshot=(572+(i*93), y_cords, 574+(i*93), y_cords+1))
            if _check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png') is True:
                print(f'Обнаружена красная шмотка в {i} слоте 1ый ряд')
                ahk.mouse_actions('move', x=575+(i*95), y=y_cords)
                ahk.mouse_actions('click')
                return False
        y_cords = 560
        for i in range(8):
            image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png', area_of_screenshot=(572+(i*93), y_cords, 574+(i*93), y_cords+1))
            if _check_red(f'{PATH_TO_ALCHEMY}\\imgs\\is_item_in_sharp_menu_red.png') is True:
                print(f'Обнаружена красная шмотка в {i} слоте 1ый ряд')
                ahk.mouse_actions('move', x=575+(i*95), y=y_cords-15)
                ahk.mouse_actions('click')
                return False
        print('Красных шмоток не найдено')
        return True

    def _exit_from_sharp_scroll():
        ahk.mouse_actions('move', x=1300, y=180)
        ahk.mouse_actions('click')
        time.sleep(1)

        ahk.mouse_actions('move', x=1785, y=180)
        ahk.mouse_actions('click')
        time.sleep(1)

    def _close_sharp_menu():
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

    def _craft_sharp_scrolls():
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

    def _find_and_open_accessory_sharp_scroll():
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
            _craft_sharp_scrolls()
            return False

    def _open_sharp_menu():
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
        if _find_and_open_accessory_sharp_scroll() is False:
            return False
        time.sleep(1.5)
        ahk.mouse_actions('move', x=1050, y=180)
        ahk.mouse_actions('click')

        time.sleep(0.5)

    def _put_items_in_sharp_scrol(amount, is_2_sharp=False):
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
            red_items = take_off_red_items_from_sharp_menu()

        if not _check_if_not_enough_scrolls_for_sharp() and image.get_amount_of_neccesary_scrolls() > 0:
            print('Недостаточно свитков для заточки бижи')
            _craft_sharp_scrolls()
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

        _exit_from_sharp_scroll()

        _close_sharp_menu()

    accessory_shapred = False
    while accessory_shapred is False:
        if _open_sharp_menu() is False:
            _close_sharp_menu()
        if _put_items_in_sharp_scrol(0) is not False:
            accessory_shapred = True


def get_inventory_info() -> str or None:
    def _check_item_in_inventory_color(row, column):
        def __check_is_item_appropriate(row, column):
            x = row
            y = column

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
                return

        y = row*100

        image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\item_in_inventory_name.png', area_of_screenshot=(1400, 50+y, 1800, 162+y+5))
        item_name = image.image_to_string(f'{PATH_TO_ALCHEMY}\\imgs\\item_in_inventory_name.png', False, False).split('\n')
        print('Название шмотки без обработки', item_name)

        if __check_is_item_appropriate(row, column) is False:
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
            return

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

        if image.is_item_color_blue('blue.png'):
            print('Blue')

            #item_name = image.image_to_string('blue.png', False, False)
            print(f'item name from blue template is {item_name}')

            if __check_is_item_appropriate(row, column) is False:
                print(item_name, 'Нельзя положить')
                return

            print('item_name is ', item_name)
            print('Название шмотки ', item_name)
            found_item = False
            LIST_OF_ACCESORIES_WORDS = ('кольцо', 'ожерелье', 'серьга', 'пояс', 'браслет', 'ожёрелье', 'глаз')
            LIST_OF_PIECE_WORDS = ('авадон', 'молнии', 'зубе', 'кронвист')

            for i in LIST_OF_ACCESORIES_WORDS:
                if i in item_name.replace('\n', '').lower():
                    if '+1' in item_name.replace('\n', '').lower():
                        print('+1 Accessory')
                        return '+1 Accessory'

            print(item_name, 'is not accessory')

            for i in LIST_OF_PIECE_WORDS:
                if i in item_name.replace('\n', '').lower():
                    if '8' in item_name.replace('\n', '').lower():
                        return 'piece'

    for column in range(1, 7):
        for row in range(1, 5):
            ahk.mouse_actions('move', x=1350 + row * 100, y=200 + column * 100)
            ahk.mouse_actions('click')
            time.sleep(0.2)

            item_type = _check_item_in_inventory_color(column, row)
            if item_type:
                ahk.mouse_actions('esc')
                return item_type
    ahk.mouse_actions('esc')


def start_side_bots():
    AutoSellBotFinal.run(None, None, path)
    script_dlya_sbora_plushek.run(5, None, path, None)


def run(hwnd):
    def _open_menu():
        image.take_screenshot('is_menu_opened.png', (1730, 180, 1820, 292))

        while not image.matching('is_menu_opened.png', 'menu_opened.png'):
            ahk.mouse_actions('move', x=1775, y=90)
            ahk.mouse_actions('click')
            time.sleep(1)
            image.take_screenshot('is_menu_opened.png', (1730, 180, 1820, 292))

    def _open_market():
        ahk.mouse_actions('move', x=1510, y=450)
        ahk.mouse_actions('click')

    def _open_sale_menu():
        ahk.mouse_actions('move', x=400, y=185)
        ahk.mouse_actions('click')

    def _open_alchemy():
        ahk.mouse_actions('move', x=1680, y=330)
        ahk.mouse_actions('click')

    try:
        acc_name = windows.get_window_name(hwnd)
        try:
            seted_roll = list(accs_and_rolls_dict[acc_name].items())[0][0]
            print(list(accs_and_rolls_dict[acc_name].items())[0][1])
        except KeyError:
            print('Этого аккаунта нет в списке')
            seted_roll = ''

        telegram = Telegram()

        items_list = None
        accesory_items_list = None

        roll_amount = 1

        if 'Roll_40' in seted_roll or 'Roll_50' in seted_roll:
            roll = seted_roll

        if 'Roll_40' not in seted_roll and 'Roll_50' not in seted_roll:
            _open_menu()
            time.sleep(2)
            _open_market()
            time.sleep(4)
            _open_sale_menu()
            time.sleep(5)

            amount_of_adena = image.get_adena_amount()
            amount_of_diamonds = image.get_diamonds_amount()
            amount_of_slots = image.get_amount_of_slots()

            print(f'Адены {amount_of_adena}')
            print(f'Алмазов {amount_of_diamonds}')
            print(f'Слотов {amount_of_slots}')

            ahk.mouse_actions('esc')
            time.sleep(1)

            sharp_accessory()
            time.sleep(2)

            if amount_of_adena < 40_000_000:
                return

            if amount_of_diamonds < 1000:
                roll = 'Roll_00().start_roll'

            elif amount_of_diamonds > 1000:
                roll = 'Roll_66().start_roll'
                if amount_of_adena < 110_000_000:
                    roll = 'Roll_66_Lite().start_roll'

            roll_amount = 30 - amount_of_slots

            #print(accs_and_rolls_dict)

            #print(f'roll {roll}')
            #roll_amount = int(list(accs_and_rolls_dict[acc_name].items())[0][1])
            print(roll_amount)

            if '40' not in roll and '50' not in roll:
                pass
                #sort_inventory()

            open(f'{PATH_TO_ALCHEMY}gained_items_list.txt', 'w').close()

            prev_roll = roll

            need_80 = False

            for i in range(roll_amount):
                _open_menu()
                time.sleep(2)
                _open_alchemy()
                time.sleep(3)
                item_type = get_inventory_info()

                match item_type:
                    case 'piece':
                        roll = 'Roll_80().start_roll'
                    case '+1 Accessory':
                        roll = 'Roll_66().start_roll'
                    case None:
                        roll = prev_roll


                items_list, accesory_items_list, roll_amount, adena_wasted, diamonds_wasted, items_bought, gained_slot, gained_item, wasted_time, need_80, need_to_change_bot = eval(roll + f'({items_list}, {accesory_items_list}, {str(roll_amount)}, {str(hwnd)})')
                print('items list is ',items_list)
                print('accesory_items_list is ', accesory_items_list)
                #telegram.send_msg_in_tg(hwnd, type='roll info', adena_wasted=adena_wasted, roll_type=roll,
                #y                        diamonds_wasted=diamonds_wasted, items_bought=items_bought, gained_slot=gained_slot, gained_item=gained_item, wasted_time=wasted_time)

                if need_to_change_bot:
                    start_side_bots()

                if roll_amount == 0:
                    return

         #   if items_list is False:
          #      telegram.send_msg_in_tg('overflow')
           #     return
        #telegram.send_msg_in_tg(hwnd, 'end')
        return

    except Exception as e:
        traceback.print_exc()
        pass

def main(path):
    windows.switch_windows(run)

if __name__ == '__main__':
    windows.switch_windows(run)