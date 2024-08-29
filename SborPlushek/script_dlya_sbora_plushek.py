from ahk import AHK
from PIL import Image as pil

import random
import time
import json

import win32gui
import win32con
import win32com.client

import pyscreenshot
import pytesseract
import numpy as np
import cv2

import psutil
import pythoncom
import telebot

import TGNotifier

import json

# AHK 0.14.2 ОБЯЗАТЕЛЬНО
# ЗАПУСК ОТ ИМЕНИ АДМИНИСТРАТОРА ОБЯЗАТЕЛЬНО

TIME_FOR_WORK = ['21:49','','']
CLAN_CLICKS = 3
MULTIPLIER = 1
PATH_TO_SCRIPT = ''

#Колличество ивентов в текущий момент
AMOUNT_OF_EVENTS = 1
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# номер данжа
NUM_OF_DUNGEON = 1

with open(f'{PATH_TO_SCRIPT}account_lvls.json') as account_lvls_json:
    account_lvls = json.load(account_lvls_json)

autohotkey = AHK()

# Класс для взаимодействия с окнами

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

        elif action == 'wheel_up':
            while True:
                try:
                    autohotkey.wheel_up()
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


# Класс для работы компьютерного зрения и изображений
class Image:
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

    def get_main_color(self, file, colors_amount=1024):
        img = pil.open(file)
        colors = img.getcolors(colors_amount)  # put a higher value if there are many colors in your image

        colors = sorted(colors)
        if (0,0,0) in colors:
            colors.remove(colors[0])
        return colors[0][1]

    def get_lvl(self) -> int or bool:
        def _prepare_lvl(lvl):
            lvl = lvl.replace(' ', '')
            lvl = lvl.replace('\n', '')
            lvl = lvl.replace('LV.', '')
            return lvl

        self.take_screenshot(f'{PATH_TO_SCRIPT}lvl.png', (90, 985, 130, 1020))

        lvl = pytesseract.image_to_string(f'{PATH_TO_SCRIPT}lvl.png', config='--psm 6 -c tessedit_char_whitelist=0123456789LV.')
        lvl = _prepare_lvl(lvl)

        print(f'current_lvl {lvl}')

        try:
            return int(lvl)
        except Exception as e:
            print(f'Не удалось получить лвл, {e}')
            return False

    def get_dungeon_name(self):
        def _prepare_dungeon_name(name) -> str:
            name = name.replace(' ', '')
            name = name.replace('\n', '')
            name = name.replace('"', '')
            name = name.replace("'", "")
            name = name.lower()
            return name

        DUNGEONS_LIST = {
            "храмундины": "UNDINA'S TEMPLE",
            "разоренныйзамок": "DEVASTATED CASTLE",
            "островнеистовства": "ISLAND OF FURY"
        }

        self.take_screenshot(f'{PATH_TO_SCRIPT}dungeon_name.png', (1210, 320, 1620, 375))

        dungeon_name = pytesseract.image_to_string(f'{PATH_TO_SCRIPT}dungeon_name.png', lang='rus', config='--psm 6 --oem 3')
        dungeon_name = _prepare_dungeon_name(dungeon_name)

        return DUNGEONS_LIST.get(dungeon_name)

# Класс для работы с окнами
ahk = AHKActions()
image = Image()
class Windows():

    def switch_windows(self, func):
        shell = win32com.client.Dispatch("WScript.Shell")

        windows_list = self.__find_windows()

        print('Спиок открытых окок с линейкой', windows_list)

        if len(windows_list) > 0:
            for window in windows_list:
                for i in range(3):
                    shell.SendKeys('%')
                try:
                    win32gui.ShowWindow(window, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(window)
                except:
                    continue

                while self.is_screen_locked() is True:
                    self.unlock_screen()
                    time.sleep(2)

                time.sleep(2*MULTIPLIER)
                if self._is_dead() is True:
                    print("Перс умер")
                    self._revive()
                    time.sleep(5*MULTIPLIER)
                func(window)

    def _is_dead(self):
        if image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg', f'{PATH_TO_SCRIPT}dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg', f'{PATH_TO_SCRIPT}dead2.png', need_for_taking_screenshot=True) is True:
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
            is_locked = image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg', f'{PATH_TO_SCRIPT}screen_is_locked.png', need_for_taking_screenshot=True)
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

    def is_there_clan(self):
        time.sleep(2)
        clan = image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg', f'{PATH_TO_SCRIPT}clan_mark.png', need_for_taking_screenshot=True)
        return clan

    def get_account_name(self, hwnd):
        account_name = win32gui.GetWindowText(hwnd)

        account_name = account_name.replace('Lineage2M l ', '')

        return account_name

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


# Класс в котором производяться все основные действия
windows = Windows()
image = Image()
ahk = AHKActions()

class Telegram:
    """Класс для взаимодействия с тг"""
    def __init__(self):
        self.TG_ID = 420909529
        self.TOKEN = '6775352589:AAG_LBg1GWil7ypCR8h_e7BhpZDCubFKbQQ'
        self.BOT = telebot.TeleBot(self.TOKEN)
        self.TIMEOUT = 3600

    def send_next_dungeon_msg(self):
        """Функция для отправки сообщения о том что пора переключать данж"""
        self.BOT.send_message(self.TG_ID, 'Пора переключить данжи')

    def send_end_msg(self):
        """Функция для отправки сообщения о том что все данжи пройдены"""
        self.BOT.send_message(self.TG_ID, 'Все данжи переставлены')

class IOOperations:
    """Класс для взаимодействия с файлами"""
    def update_current_dungeon(self, current_dungeon_num):
        with open('settings.txt') as f:
            for i in f.readlines():
                if 'SborPlushek_current_dungeon' in i:
                    current_dungeon = i.split('=')
                    break
        with open('settings.txt', 'r') as f:
            old_data = f.read()
            print(current_dungeon[1])
            new_data = old_data.replace(f'SborPlushek_current_dungeon={current_dungeon[1]}',
                                        f'SborPlushek_current_dungeon={current_dungeon_num}\n')
        with open('settings.txt', 'w') as f:
            f.write(new_data)

io = IOOperations()

class InGame():
    def lock_window(self):
        ahk.mouse_actions('move', x=70, y=640)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=940, y=550)
        ahk.mouse_actions('click')
        time.sleep(2)

    def unlock_window(self):
        windows.unlock_screen()
        time.sleep(1)

    def respawn(self):
        ahk.mouse_actions('move', x=928, y=865)
        ahk.mouse_actions('click')

    def go_to_menu(self):
        ahk.mouse_actions('move', x=1775, y=80)
        ahk.mouse_actions('click')

    def go_to_adena_shop(self):
        ahk.mouse_actions('move', x=1425, y=90)
        ahk.mouse_actions('click')

        while image.matching(f'{PATH_TO_SCRIPT}is_there_adena_shop_cross.png', f'{PATH_TO_SCRIPT}cross_adena_shop.png',
                             need_for_taking_screenshot=True, threshold=0.7, area_of_screenshot=(1510, 765, 1555, 815)) is False:
            time.sleep(0.1)
            print('Нету крестика для того чтобы закрыть рекламу, ждемс')

        ahk.mouse_actions('move', x=1530, y=780)
        ahk.mouse_actions('click')
        time.sleep(3)

        ahk.mouse_actions('move', x=400, y=180)
        ahk.mouse_actions('click')


    def in_adena_shop_buy_all(self):
        y_cords_to_shop = 290
        for i in range(4):
            ahk.mouse_actions('move', x=1700, y=y_cords_to_shop)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=1580, y=980)
            ahk.mouse_actions('click')
            y_cords_to_shop += 90
            if image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg', f'{PATH_TO_SCRIPT}adena_shop_nothing_to_buy.png', need_for_taking_screenshot=True) is True:
                ahk.mouse_actions('esc')

            else:
                ahk.mouse_actions('move', x=1070, y=885)
                ahk.mouse_actions('click')

                time.sleep(4*MULTIPLIER)
        ahk.mouse_actions('move', x=1800, y=80)
        ahk.mouse_actions('click')

    def go_to_clan_menu(self):
        ahk.mouse_actions('move', x=1515, y=570)
        ahk.mouse_actions('click')

    def check_for_clan(self):
        if windows.is_there_clan() is True:


            ahk.mouse_actions('move', x=850, y=950)
            ahk.mouse_actions('click')

            for i in range(CLAN_CLICKS):
                ahk.mouse_actions('move', x=500, y=800)
                ahk.mouse_actions('click')

                ahk.mouse_actions('move', x=1070, y=690)
                ahk.mouse_actions('click')

            ahk.mouse_actions('esc')

            ahk.mouse_actions('move', x=500, y=750)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)

            ahk.mouse_actions('esc')
        else:
            ahk.mouse_actions('esc')

    def go_to_mail(self):
        ahk.mouse_actions('move', x=1430, y=830)
        ahk.mouse_actions('click')

    def get_all_rewards_from_mail(self):
        ahk.mouse_actions('move', x=1565, y=950)
        ahk.mouse_actions('click')
        time.sleep(10*MULTIPLIER)

        ahk.mouse_actions('move', x=800, y=700)
        ahk.mouse_actions('click')

        ahk.mouse_actions('esc')
        time.sleep(2*MULTIPLIER)

    def go_to_battle_pass_menu(self):
        ahk.mouse_actions('move', x=1515, y=820)
        ahk.mouse_actions('click')

    def get_all_battle_pass_rewards(self):
        def __get_rewards():
            while image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg', f'{PATH_TO_SCRIPT}get_reward.png', need_for_taking_screenshot=True,
                                  area_of_screenshot=(1225, 270, 1375, 370), threshold=0.7) is True:
                ahk.mouse_actions('move', x=1300, y=320)
                ahk.mouse_actions('click')
                time.sleep(1)

            return True

        y_cords_battle_pass_reward = 290

        for i in range(2):
            ahk.mouse_actions('move', x=90, y=y_cords_battle_pass_reward)
            ahk.mouse_actions('click')

            __get_rewards()

            ahk.mouse_actions('move', x=1450, y=950)
            ahk.mouse_actions('click')
            ahk.mouse_actions('move', x=990, y=700)
            ahk.mouse_actions('click')

            y_cords_battle_pass_reward += 90

        ahk.mouse_actions('move', x=1800, y=80)
        ahk.mouse_actions('click')

        time.sleep(2)

    def go_to_bonus_menu(self):
        ahk.mouse_actions('move', x=1700, y=575)
        ahk.mouse_actions('click')

    def get_bonuses_from_bonus_menu(self):
        def __collect_bonus():
            ahk.mouse_actions('move', x=1400, y=560)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=1070, y=705)
            ahk.mouse_actions('click')
            time.sleep(2*MULTIPLIER)

        counter = 0
        for i in range(7):
            image.take_screenshot(f'{PATH_TO_SCRIPT}\\is_bonus_available.png', area_of_screenshot=(1600, 200+counter, 1830, 310+counter))
            if image.matching(f'{PATH_TO_SCRIPT}\\is_bonus_available.png', f'{PATH_TO_SCRIPT}\\end_of_bonuses.png', threshold=0.8) is True:
                break

            ahk.mouse_actions('move', x=1700, y=250+counter)
            ahk.mouse_actions('click')
            time.sleep(1)
            image.take_screenshot(f'{PATH_TO_SCRIPT}\\is_there_cristals.png', area_of_screenshot=(1250, 525, 1575, 600))
            if image.matching(f'{PATH_TO_SCRIPT}\\is_there_cristals.png', f'{PATH_TO_SCRIPT}\\cristal_in_bonuses.png', threshold=0.7) is True:
                pass
            else:
                for i in range(2):
                    __collect_bonus()

            counter += 110

        ahk.mouse_actions('move', x=1800, y=80)
        ahk.mouse_actions('click')

    def go_to_town(self):
        time.sleep(2)
        ahk.mouse_actions('move', x=180, y=250)
        ahk.mouse_actions('click')

        time.sleep(2)

        for i in range(2):
            ahk.mouse_actions('move', x=100, y=200)
            ahk.mouse_actions('click')
            time.sleep(2)

        ahk.mouse_actions('move', x=180, y=200)
        ahk.mouse_actions('click')

        time.sleep(2)
        ahk.mouse_actions('move', x=250, y=315)
        ahk.mouse_actions('click')

        time.sleep(2)
        ahk.mouse_actions('move', x=1615, y=700)
        ahk.mouse_actions('click')

        time.sleep(2)
        ahk.mouse_actions('move', x=1100, y=700)
        ahk.mouse_actions('click')

        time.sleep(5)

    def open_sellers_menu(self):
        image.take_screenshot(f'{PATH_TO_SCRIPT}\\is_sellers_menu_opened.png', (45, 150, 315, 325))

        ahk.mouse_actions('move', x=350, y=280)
        ahk.mouse_actions('click')
        time.sleep(1)

        image.take_screenshot(f'{PATH_TO_SCRIPT}\\is_sellers_menu_opened_1.png', (45, 150, 315, 325))

        while image.matching(f'{PATH_TO_SCRIPT}\\is_sellers_menu_opened.png', f'{PATH_TO_SCRIPT}\\is_sellers_menu_opened_1.png') is True:
            ahk.mouse_actions('move', x=350, y=280)
            ahk.mouse_actions('click')
            time.sleep(1)

            image.take_screenshot(f'{PATH_TO_SCRIPT}\\is_sellers_menu_opened_1.png', (45, 150, 315, 325))

    def _autoselling(self):
        ahk.mouse_actions('move', x=1490, y=940)
        ahk.mouse_actions('click')
        no_tg_notifications = False
        while no_tg_notifications is False:
            image.take_screenshot(f'{PATH_TO_SCRIPT}\\are_there_tg_notifications.png', area_of_screenshot=(1690, 934, 1691, 935))
            color = image.get_main_color(f'{PATH_TO_SCRIPT}\\are_there_tg_notifications.png')
            if (90 < color[0] < 120) and (40 < color[1] < 60) and (0 < color[2] < 15):
                ahk.mouse_actions('move', x=1700, y=950)
                ahk.mouse_actions('click')
                no_tg_notifications = True
            elif (190 < color[0] < 230) and (90 < color[1] < 120) and (0 < color[2] < 25):
                ahk.mouse_actions('move', x=1700, y=950)
                ahk.mouse_actions('click')
                no_tg_notifications = True
            else:
                ahk.mouse_actions('move', x=1500, y=950)
                print('Обнаруженно сообщение в тг, ожидает секунду')
                time.sleep(1)

        ahk.mouse_actions('move', x=1080, y=710)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1800, y=80)
        ahk.mouse_actions('click')

    def go_to_sellers(self):

        grocer_x = 200
        grocer_y = 180

        buyer_x = 200
        buyer_y = 310

        warehouse_worker_x = 200
        warehouse_worker_y = 440

        if AMOUNT_OF_EVENTS > 0:
            if (image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg', f'{PATH_TO_SCRIPT}event_mark.png',
                              need_for_taking_screenshot=True, threshold=0.8)) or (image.matching(f'{PATH_TO_SCRIPT}main_screen.jpg',
                                                                                                  f'{PATH_TO_SCRIPT}event_mark_1.png',
                                                                                                  need_for_taking_screenshot=True,
                                                                                                  threshold=0.75)) is True:
                statue_x = 200
                statue_y = 180

                grocer_x = 200
                grocer_y = 240

                buyer_x = 200
                buyer_y = 500

                warehouse_worker_x = 200
                warehouse_worker_y = 370

                if AMOUNT_OF_EVENTS == 1:
                    event_x = 200
                    event_y = 180

                    grocer_x = 200
                    grocer_y = 240

                    buyer_x = 200
                    buyer_y = 500

                    warehouse_worker_x = 200
                    warehouse_worker_y = 370

                    ahk.mouse_actions('move', x=event_x, y=event_y)
                    ahk.mouse_actions('click')
                    time.sleep(13)
                    ahk.mouse_actions('move', x=1080, y=700)
                    ahk.mouse_actions('click')
                    print("Пришел к ивенту")

                if AMOUNT_OF_EVENTS == 2:
                    event_x = 200
                    event_y = 180

                    second_event_x = 200
                    second_event_y = 240

                    grocer_x = 200
                    grocer_y = 300

                    buyer_x = 200
                    buyer_y = 500

                    warehouse_worker_x = 200
                    warehouse_worker_y = 450

                    ahk.mouse_actions('move', x=event_x, y=event_y)
                    ahk.mouse_actions('click')
                    time.sleep(13)
                    #self._autoselling()
                    ahk.mouse_actions('move', x=1390, y=950)
                    ahk.mouse_actions('click')

                    for _ in range(2):
                        ahk.mouse_actions('move', x=630, y=630)
                        ahk.mouse_actions('click')
                        time.sleep(1)

                    ahk.mouse_actions('move', x=1650, y=950)
                    ahk.mouse_actions('click')

                    ahk.mouse_actions('move', x=950, y=710)
                    ahk.mouse_actions('click')

                    ahk.mouse_actions('esc')
                    print("Пришел к ивенту")

                    ahk.mouse_actions('move', x=second_event_x, y=second_event_y)
                    ahk.mouse_actions('click')
                    time.sleep(13)
                    ahk.mouse_actions('move', x=1080, y=700)
                    ahk.mouse_actions('click')
                    print("Пришел ко второму ивенту")

                    ahk.mouse_actions('move', x=grocer_x, y=grocer_y)
                    ahk.mouse_actions('click')
                    time.sleep(13 * MULTIPLIER)
                    self._autoselling()
                    print("Пришел к бакалейщику")

                    ahk.mouse_actions('move', x=warehouse_worker_x, y=warehouse_worker_y)
                    # for i in range(2):
                    #    ahk.mouse_actions('wheel')
                    ahk.mouse_actions('click')
                    time.sleep(13 * MULTIPLIER)
                    self._autoselling()
                    print("Пришел к рабочему склада")
                    ahk.mouse_actions('move', x=warehouse_worker_x, y=warehouse_worker_y)
                    for _ in range(2):
                        ahk.mouse_actions('wheel')
                    ahk.mouse_actions('move', x=buyer_x, y=buyer_y)
                    ahk.mouse_actions('click')
                    time.sleep(13 * MULTIPLIER)
                    self._autoselling()
                    print("Пришел к скупщику")

                    ahk.mouse_actions('move', x=buyer_x, y=buyer_y)
                    for _ in range(2):
                        ahk.mouse_actions('wheel_up')

                    return
            else:
                grocer_x = 200
                grocer_y = 180

                buyer_x = 200
                buyer_y = 440

                warehouse_worker_x = 200
                warehouse_worker_y = 300

        # go_to_warehouse_worker
        ahk.mouse_actions('move', x=warehouse_worker_x, y=warehouse_worker_y)
        #for i in range(2):
        #    ahk.mouse_actions('wheel')
        ahk.mouse_actions('click')
        time.sleep(13*MULTIPLIER)
        self._autoselling()
        print("Пришел к рабочему склада")

        #go_to_grocer
        ahk.mouse_actions('move', x=grocer_x, y=grocer_y)
        ahk.mouse_actions('click')
        time.sleep(13*MULTIPLIER)
        self._autoselling()
        print("Пришел к бакалейщику")

        #go_to_buyer
        if AMOUNT_OF_EVENTS == 2:
            pass

        ahk.mouse_actions('move', x=buyer_x, y=buyer_y)
        ahk.mouse_actions('click')
        time.sleep(13*MULTIPLIER)
        self._autoselling()
        print("Пришел к скупщику")

    def switch_off_fast_walk_to_sellers(self):
        ahk.mouse_actions('move', x=200, y=300)
        for i in range(2):
            ahk.mouse_actions('wheel_up')
        ahk.mouse_actions('move', x=350, y=270)
        ahk.mouse_actions('click')

    def tp_to_previous_location(self):
        ahk.mouse_actions('move', x=350, y=175)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=200, y=340)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=420, y=460)
        ahk.mouse_actions('click')

        time.sleep(3*MULTIPLIER)

        ahk.mouse_actions('move', x=1525, y=550)
        ahk.mouse_actions('click')

    def go_to_dungeon_menu(self):
        ahk.mouse_actions('move', x=1580, y=450)
        ahk.mouse_actions('click')

    def choose_dungeon(self):
        ahk.mouse_actions('move', x=390, y=150+(NUM_OF_DUNGEON*200))
        ahk.mouse_actions('click')

    def _choose_dungeon_lvl(self, hwnd, acc_lvl: int):
        def _get_dungeon_lvls_file() -> dict:
            with open('SborPlushek\\dungeon_lvls.json') as text:
                return json.load(text)

        dungeon_type = image.get_dungeon_name()
        need_to_find_lvl = True
        if dungeon_type is not False:
            print(f"Данж обнаружен в списке {dungeon_type}")
            lvls_file = _get_dungeon_lvls_file()
            print(f'lvls_file {lvls_file}')

            lvls_list = lvls_file.get(dungeon_type)
            print(f'lvls_list {lvls_list}')
            if lvls_list:
                for c in lvls_list.items():
                    lvls = c[0].split('-')
                    print(f'lvls {lvls}')
                    if int(lvls[0]) <= acc_lvl <= int(lvls[1]):
                        lvl = c[1]
                        print(f'Данж обнаружен. Выбран лвл {lvl}')
                        need_to_find_lvl = False
            else:
                print('Данж не обнаружен в списке')
        else:
            print('Данж не обнаружен в списке')

        ahk.mouse_actions('move', x=1350, y=950)
        ahk.mouse_actions('click')

        if need_to_find_lvl:
            account_name = windows.get_account_name(hwnd)
            print(account_name)
            lvl = 0
            for i in account_lvls.keys():
                print(i)
                if account_name == i:
                    print(123)
                    lvl = account_lvls[i]
            if lvl == 0:
                print(account_name, 'нет в списке. Выбран 50 лвл по дефолту')
                lvl = 50
        return lvl

    def go_to_dungeon(self, hwnd, acc_lvl):
        def __click_on_dungeon_lvl_button(x, y):
            ahk.mouse_actions('move', x=x, y=y)
            ahk.mouse_actions('click')

        lvl = self._choose_dungeon_lvl(hwnd, acc_lvl)
        print(lvl)
        if lvl == 30:
            __click_on_dungeon_lvl_button(x=1200, y=270)
        elif lvl == 40:
            __click_on_dungeon_lvl_button(x=1200, y=270)
        elif lvl == 50:
            __click_on_dungeon_lvl_button(x=1200, y=370)
        elif lvl == 55:
            __click_on_dungeon_lvl_button(x=1200, y=470)
        elif lvl == 60:
            __click_on_dungeon_lvl_button(x=1200, y=570)
        elif lvl == 70:
            __click_on_dungeon_lvl_button(x=1200, y=670)


ingame = InGame()
# Основная часть программы
def main(hwnd):
    ingame.lock_window()
    time.sleep(2)
    lvl = image.get_lvl()
    ingame.unlock_window()

    if NUM_OF_DUNGEON == 1:
        ingame.go_to_menu()
        ingame.go_to_adena_shop()
        time.sleep(1)
        ingame.in_adena_shop_buy_all()

        ingame.go_to_menu()
        ingame.go_to_clan_menu()
        ingame.check_for_clan()

        ingame.go_to_menu()
        ingame.go_to_mail()
        ingame.get_all_rewards_from_mail()

        ingame.go_to_menu()
        time.sleep(1)
        ingame.go_to_bonus_menu()
        ingame.get_bonuses_from_bonus_menu()
        ingame.go_to_town()
        ingame.open_sellers_menu()
        ingame.go_to_sellers()
        ingame.switch_off_fast_walk_to_sellers()
        ingame.go_to_menu()

        ingame.go_to_battle_pass_menu()
        time.sleep(1)
        ingame.get_all_battle_pass_rewards()

        ingame.tp_to_previous_location()

    ingame.go_to_menu()
    ingame.go_to_dungeon_menu()
    ingame.choose_dungeon()
    ingame.go_to_dungeon(hwnd, lvl)
    time.sleep(6*MULTIPLIER)
    windows.lock_screen()

telegram = Telegram()

def start():
    global NUM_OF_DUNGEON
    pythoncom.CoInitializeEx(0)

    now = time.localtime()
    current_time = time.strftime("%H:%M", now)
    print(current_time)

    if NUM_OF_DUNGEON > 3:
        print('Бот сделан только для 3 данжей(((((( 4го нетю(')
        return
    if current_time in TIME_FOR_WORK:
        windows.switch_windows(main)

    elif 'Авто' in TIME_FOR_WORK:
        windows.switch_windows(main)

        io.update_current_dungeon(NUM_OF_DUNGEON+1)

        time.sleep(telegram.TIMEOUT)
        telegram.send_next_dungeon_msg()

        if NUM_OF_DUNGEON == 3:
            telegram.send_end_msg()
            return

def run(clan_clicks, multiplier, path, schedule, current_dungeon):
    global CLAN_CLICKS
    global MULTIPLIER
    global PATH_TO_SCRIPT
    global TIME_FOR_WORK
    global NUM_OF_DUNGEON

    CLAN_CLICKS = int(clan_clicks)
    NUM_OF_DUNGEON = int(current_dungeon)
    MULTIPLIER = int(multiplier)
    PATH_TO_SCRIPT = f'{path}\\SborPlushek\\'

    TIME_FOR_WORK = ('Авто')

    print(TIME_FOR_WORK)

    start()

def collect_apples(window):
    def _go_to_event_seller():
        ahk.mouse_actions('move', x=140, y=190)
        ahk.mouse_actions('click')

    def _add_item(x, y):
        ahk.mouse_actions('move', x, y)
        ahk.mouse_actions('click')

    def _set_max():
        ahk.mouse_actions('move', 730, 960)
        ahk.mouse_actions('click')

    ingame.go_to_town()

    ingame.open_sellers_menu()
    _go_to_event_seller()

    time.sleep(12)

    _add_item(125, 330)
    _set_max()

    _add_item(125, 450)
    _set_max()

    ahk.mouse_actions('move', 1620, 950)
    ahk.mouse_actions('click')

    ahk.mouse_actions('move', 950, 720)
    ahk.mouse_actions('click')

    ahk.mouse_actions('esc')

    ingame.open_sellers_menu()

    windows.lock_screen()

def start_collect_apples(path):
    try:
        global PATH_TO_SCRIPT
        PATH_TO_SCRIPT = f'{path}\\SborPlushek\\'
        windows.switch_windows(collect_apples)
    except Exception as e:
        TGNotifier.send_break_msg('Сбор плюшек яблоки', '', e)

def collect_event_good(hwnd):
    def _click_on_good():
        ahk.mouse_actions('move', x=220, y=450)
        ahk.mouse_actions('click')

    def _buy_good():
        ahk.mouse_actions('move', x=980, y=790)
        ahk.mouse_actions('click')

    ingame.go_to_adena_shop()
    _click_on_good()
    _buy_good()

    ahk.mouse_actions('move', x=1790, y=90)
    ahk.mouse_actions('click')

    time.sleep(1)

    windows.lock_screen()

def start_collect_event_good(path):
    try:
        global PATH_TO_SCRIPT
        PATH_TO_SCRIPT = f'{path}\\SborPlushek\\'
        windows.switch_windows(collect_event_good)
    except Exception as e:
        TGNotifier.send_break_msg('Сбор плюшек ивент', '', e)
