from ahk import AHK
from PIL import Image as pil
from termcolor import colored, cprint

import psutil

import PIL.ImageGrab
import numpy as np
import cv2
import pytesseract

import win32gui
import win32com.client
import win32con

import telebot

import random
import time
import json


IS_THERE_EVENT = True

PATH_TO_DUNGEON_MASTER = r'C:\Users\MIFIKUS\PycharmProjects\BigBot\DungeonMaster\\'
ACCOUNTS_AND_DUNGEONS_LVLS = None
ACCOUNTS_LIST = None

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
autohotkey = AHK()

class AHKActions:
    """Класс для работы с AHK"""
    def mouse_actions(self, action, x=0, y=0):
        """Функция для работы с AHK"""
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
                    time.sleep(0.15)
                    autohotkey.click(direction='U')
                    break
                except Exception:
                    pass
            time.sleep(0.2)
            return

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

        try:
            for proc in psutil.process_iter():
                if proc.name() == 'AutoHotkey.exe':
                    proc.kill()
        except Exception as e:
            print(e)
            print("AHK process doesn't exists anymore")

ahk = AHKActions()

class Image:
    """Класс для работы с изображениями"""
    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):
        """Функция для поиска совпадений между двумя изображениями"""
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
        """Функция для создания скриншотов"""
        if area_of_screenshot:
            PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
        else:
            PIL.ImageGrab.grab().save(image_name)

    def image_to_string(self, image_name, is_digits, fill_diamond=True):
        """Функция для перевода картинки в строку"""
        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789/')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 3')
        return text

    def check_if_there_is_error_after_unlock_window(self):
        """Функция для проверки есть ли ошибка после разблокировки окна"""
        self.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_there_error_button.png', area_of_screenshot=(550, 420,
                                                                                                               1250, 800))
        is_there_error = self.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_there_error_button.png',
                                       f'{PATH_TO_DUNGEON_MASTER}\\imgs\\error_after_unlock_button.png',
                                       need_for_taking_screenshot=False, threshold=0.7)

        if is_there_error:
            ahk.mouse_actions('move', x=950, y=620)
            ahk.mouse_actions('click')
            time.sleep(3)

    def get_main_color(self, file, colors_amount=1024):
        """Функция для полчения цвета который больше всего встречается на картинке"""
        img = pil.open(file)
        colors = img.getcolors(colors_amount)
        colors = sorted(colors)
        if (0,0,0) in colors:
            colors.remove(colors[0])
        return colors[0][1]

image = Image()

class Windows():
    """Класс для работы с окнами"""
    def switch_windows(self, func, current_time):
        """Функциыя для переключения окон"""
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
                        image.check_if_there_is_error_after_unlock_window()
                if self._is_dead() is True:
                    self._revive()
                    time.sleep(5)
                func(window, current_time)

    def get_acc_name(self, hwnd):
        acc_name = win32gui.GetWindowText(hwnd)
        acc_name = acc_name.replace('Lineage2M l ', '')

        if 'Lineage2M' not in acc_name:
            return acc_name

        for i in range(5):
            image.take_screenshot(f"{PATH_TO_AUTOSELL}acc_name.png", area_of_screenshot=(150, 0,
                                                                                         300, 40))
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
            image.take_screenshot(f"{PATH_TO_AUTOSELL}acc_name.png", area_of_screenshot=(1200, 265,
                                                                                         1445, 315))
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

    def _is_dead(self):
        """Фуцнкия для проверки мертв ли персонаж"""
        image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\main_screen.jpg')
        if image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\main_screen.jpg', f'{PATH_TO_DUNGEON_MASTER}\\imgs\\dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\main_screen.jpg', f'{PATH_TO_DUNGEON_MASTER}\\imgs\\dead2.png', need_for_taking_screenshot=True) is True:
            return True

    def _revive(self):
        """Функция для возрождения персонажа"""
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
        image.take_screenshot('amount_of_free_revives.png', area_of_screenshot=(385, 600,
                                                                                420, 640))
        try:
            amount_of_free_revives = int(pytesseract.image_to_string('amount_of_free_revives.png',
                                                                     config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
        except:
            ahk.mouse_actions('move', x=1050, y=700)
            ahk.mouse_actions('click')

            __send_to_last_location()
            return

        print(amount_of_free_revives)
        while image.matching('is_items_lose_via_death.png', 'adena.png', need_for_taking_screenshot=True, area_of_screenshot=(430, 600,
                                                                                                                              480, 650)) is False:
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

        while image.matching('is_items_lose_via_death.png', 'adena.png', need_for_taking_screenshot=True, area_of_screenshot=(430, 600,
                                                                                                                              480, 650)) is False:
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
        """Фукнция для проверки заблокировано ли окно"""
        for i in range(2):
            is_locked = image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\main_screen.jpg', f'{PATH_TO_DUNGEON_MASTER}\\imgs\\screen_is_locked.png', need_for_taking_screenshot=True)
        return is_locked

    def unlock_screen(self):
        """Функция для разблокировки окна"""
        ahk.mouse_actions('move', x=960, y=540)
        ahk.mouse_actions('drag', x=100, y=100)

    def lock_screen(self):
        """Функция для блокировки окна"""
        ahk.mouse_actions('move', x=73, y=633)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('move', x=960, y=540)
        ahk.mouse_actions('click')

    def __find_windows(self, window_name='Lineage2M'):
        """Фуцнция для поиска всех окон линейки"""
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

class Telegram:
    """Класс для отправки сообщений в тг"""
    def __init__(self):
        self.TG_ID = 760238501
        self.TOKEN_FOR_NOTIFATION_CHAT = '6742229208:AAGYXzPrhpstmxT_4H0WdzzA6pENlCOrAiI'
        self.TOKEN_FOR_ERROR_CHAT = '6701712211:AAEviSZtD1l1keMa6zTEnnJUjIJKqWL-PQY'

        self.NOTIFICATION_BOT = telebot.TeleBot(self.TOKEN_FOR_NOTIFATION_CHAT)
        self.ERROR_BOT = telebot.TeleBot(self.TOKEN_FOR_ERROR_CHAT)

        self.TIMEOUT_BEFORE_SEND_TO_DUNGEON_MSG = 300

    def send_notification_before_send_to_dungeon(self, time):
        """Функция для отправки уведомления о том
        что персонажам нужно поменять данж"""
        self.NOTIFICATION_BOT.send_message(self.TG_ID, f'Через {time} нужно переключить данжи')

    def send_error_message(self, error, place):
        """Функция для отправки сообщения об ошибке в тг"""
        self.ERROR_BOT.send_message(self.TG_ID, f'ОШИБКА\n'
                                                f'{error}\n'
                                                f'МЕСТО\n'
                                                f'{place}')

    def send_error_message_with_photo(self, photo, error, place):
        """Функция для отправки сообщения об ошибке в тг, с приложенной картинкой"""
        self.ERROR_BOT.send_photo(self.TG_ID, open(photo,  'rb'), f'ОШИБКА\n'
                                                                  f'{error}\n'
                                                                  f'МЕСТО\n'
                                                                  f'{place}')

    def send_end_message(self):
        """Функция для отправки сообщения в тг о том
        что все данжи пройдены"""
        self.NOTIFICATION_BOT.send_message(self.TG_ID, 'Все данжи пройдены!')

class Dungeons:
    """Координаты куда нажимать для каждого данжа"""
    DUNGEONS_CORDS_IN_MENU = {
        1: (700, 350),
        2: (700, 600),
        3: (700, 780)
    }

    if IS_THERE_EVENT:
        DUNGEON_NUMS_IN_MENU = {
            'EVENT': 1,
            'FRENZY_ISLAND': 2,
            'DEVASTATED_CASTLE': 3,
            'TEMPLE_OF_DAWN': 1,
            'KRUMAS_TOWER': 2,
            'ANTARASES_LAIR': 3,
            'IVORY_TOWER': 3
        }

    else:
        DUNGEON_NUMS_IN_MENU = {
            'FRENZY_ISLAND': 1,
            'DEVASTATED_CASTLE': 2,
            'TEMPLE_OF_DAWN': 3,
            'KRUMAS_TOWER': 1,
            'ANTARASES_LAIR': 2,
            'IVORY_TOWER': 3
        }

    EVENT_DUNGEON_CORDS = {
        30: (1200, 260),
        50: (1200, 360),
        55: (1200, 440),
        60: (1200, 540),
        70: (1200, 630)
    }
    FRENZY_ISLAND_CORDS = {
        40: (1200, 260),
        50: (1200, 360),
        55: (1200, 440),
        60: (1200, 540),
        70: (1200, 630),
        78: (1200, 710)
    }
    DEVASTATED_CASTLE_CORDS = {
        40: (1200, 260),
        50: (1200, 360),
        55: (1200, 440),
        60: (1200, 540),
        70: (1200, 630),
        78: (1200, 710)
    }
    TEMPLE_OF_DAWN_CORDS = {
        40: (1200, 260),
        50: (1200, 360),
        55: (1200, 440),
        60: (1200, 540),
        70: (1200, 630),
        78: (1200, 710)
    }
    KRUMAS_TOWER_CORDS = {
        1: (1200, 260),
        2: (1200, 360),
        3: (1200, 440),
        4: (1200, 540),
        5: (1200, 630),
        6: (1200, 710),
        7: (1200, 800)
    }
    ANTARASES_LAIR_CORDS = {
        1: (1200, 260),
        4: (1200, 360),
        5: (1200, 440),
        6: (1200, 540)
    }
    IVORY_TOWER_CORDS = {
        1: (1200, 260),
        2: (1200, 360),
        3: (1200, 440)
    }

    DUNGEON_NAMES = {
        'EVENT': EVENT_DUNGEON_CORDS,
        'FRENZY_ISLAND': FRENZY_ISLAND_CORDS,
        'DEVASTATED_CASTLE': DEVASTATED_CASTLE_CORDS,
        'TEMPLE_OF_DAWN': TEMPLE_OF_DAWN_CORDS,
        'KRUMAS_TOWER': KRUMAS_TOWER_CORDS,
        'ANTARASES_LAIR': ANTARASES_LAIR_CORDS,
        'IVORY_TOWER': IVORY_TOWER_CORDS
    }

windows = Windows()
telegram = Telegram()
dungeons = Dungeons()

class DungeonMasterHandler:
    """Класс для отлавливания багов"""
    def is_account_name_valid(self, acc_name):
        """фукнция для отлавливания бага что бот
        не смог опередилть название акка"""
        if acc_name not in ACCOUNTS_LIST:
            telegram.send_error_message(f'Аккаунта {acc_name} нет в списке аккаунтов. Установлены дефолтные лвла для данжей', '')
            print(f'Аккаунта {acc_name} нет в списке аккаунтов. Установлены дефолтные лвла для данжей')
            return False
        return True

    def is_file_available(self, file):
        """Проверка на то можно ли открыть файл"""
        try:
            open(file)
            return True
        except Exception as e:
            telegram.send_error_message(f'Нельзя открыть файл {file}\n {e}', '')
            raise Exception(f'Невозможно отырыть файл {file}')

    def is_dungeon_availiable(self, dungeon_num):
        """Функция для проверки доступен ли данж"""
        def __is_out_of_main_time(dungeon_num):
            """Функция для проверки истекло ли основное время для похода в данж"""
            image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_there_any_main_time_for_dungeon.png', area_of_screenshot=(675, 250+(dungeon_num*110),
                                                                                                                                 770, 290+(dungeon_num*110)))
            out_of_time = image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_there_any_main_time_for_dungeon.png',
                                         f'{PATH_TO_DUNGEON_MASTER}\\imgs\\dungeon_unavailiable.png',
                                         threshold=0.8, need_for_taking_screenshot=False)
            if out_of_time:
                print(f'В данже {dungeon_num} нету доступного времени')
                return True
            return False

        def __is_out_of_additional_time(dungeon_num):
            """Функция для проверки истекло ли дополнительное время для похода в данж"""
            image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_there_any_additional_time_for_dungeon.png', area_of_screenshot=(675, 280+(dungeon_num*110),
                                                                                                                                       770, 315+(dungeon_num*110)))
            out_of_time = image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_there_any_additional_time_for_dungeon.png',
                                         f'{PATH_TO_DUNGEON_MASTER}\\imgs\\dungeon_unavailiable.png',
                                         threshold=0.8, need_for_taking_screenshot=False)

            if out_of_time:
                print(f'В данже {dungeon_num} нету доступного дополнительного времени')
                return True
            return False

        if __is_out_of_main_time(dungeon_num) and __is_out_of_additional_time(dungeon_num):
            print(f'Данж под номером {dungeon_num} не доступен')
            return False

        print(f'Данж под номером {dungeon_num} доступен')
        return True

    def is_dungeon_menu_opened(self):
        """Функция для проверки открылось ли меню данжей"""
        image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_dungeon_menu_opened.png', area_of_screenshot=(1450, 65,
                                                                                                                 1740, 125))

        is_menu_opened = image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_dungeon_menu_opened.png',
                                        f'{PATH_TO_DUNGEON_MASTER}\\imgs\\dungeon_menu_opened.png',
                                        need_for_taking_screenshot=False)

        if is_menu_opened is True:
            print('Меню выбора данжа открыто')
            return True
        print('Меню выбора данжа не открыто')
        return False

    def is_lvl_menu_opened(self):
        """Функция для проверки открыто ли меню выбора лвла"""
        image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_lvl_menu_opened.png', area_of_screenshot=(625, 160,
                                                                                                             895, 220))

        menu_opened = image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_lvl_menu_opened.png',
                                     f'{PATH_TO_DUNGEON_MASTER}\\imgs\\lvl_menu_opened.png',
                                     need_for_taking_screenshot=False)

        if menu_opened is True:
            print('Меню выбора лвла для данжа открыто')
            return True
        print('Меню выбора данжа не открыто')
        return False

    def is_tp_to_dungeon_comleted(self):
        """Функция для проверки телепортировался ли персонаж в данж"""
        image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_tp_to_dungeon_completed.png', area_of_screenshot=(45, 685,
                                                                                                                     90, 730))

        tp_completed = image.matching(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_tp_to_dungeon_completed.png',
                                      f'{PATH_TO_DUNGEON_MASTER}\\imgs\\tp_to_dungeon_completed.png',
                                      need_for_taking_screenshot=False)

        if tp_completed is True:
            print('Tп в данж удалось')
            return True
        print('Тп в данж не удалось')
        return False

handler = DungeonMasterHandler()

class IngameActons:
    """Действия в игре"""
    def __init__(self):
        self.DEFAULT_LVL_TO_SEND = 50
        self.DEFAULT_LVL_TO_SEND_IN_ANTARAS_LIKE_DUNGEONS = 1
        self.ANTARAS_LIKE_DUNGEONS_NAMES = ('TEMPLE_OF_DAWN', 'KRUMAS_TOWER', 'ANTARASES_LAIR', 'IVORY_TOWER')

    def go_to_dungeon(self, dungeon, lvl):
        """Функция для перехода в данж"""
        print('Required dungeon name is', dungeon)
        print('Required dungen lvl is', lvl)

        dungeon_num = dungeons.DUNGEON_NUMS_IN_MENU.get(dungeon)

        if dungeon_num is None:
            telegram.send_error_message(f'Невозможно получить номер данжа {dungeon}', 'IngameActons.go_to_dungeon.dungeon_num')
            raise Exception(f'Невозможно получить номер данжа {dungeon}')

        dungeon_cords = dungeons.DUNGEONS_CORDS_IN_MENU.get(dungeon_num)

        if dungeon_cords is None:
            telegram.send_error_message(f'Невозможно получить координаты данжа на который надо нажать. Данж {e}', 'IngameActons.go_to_dungeon.dungeon_cords')
            raise Exception(f'Невозможно получить координаты данжа на который надо нажать. Данж {e}')

        print('Dungeon num is', dungeon_num)
        print('Dungeon cords is', dungeon_cords)

        all_lvls_cords = dungeons.DUNGEON_NAMES.get(dungeon)

        if all_lvls_cords is None:
            telegram.send_error_message(f'Невозможно получить координаты лвлов данжа {dungeon}', 'IngameActons.go_to_dungeon.all_lvls_cords')
            raise Exception(f'Невозможно получить координаты данжа на который надо нажать. Данж {e}')

        print('All lvls cords is', all_lvls_cords)

        lvl_cords = all_lvls_cords.get(lvl)
        print(lvl_cords)
        if lvl_cords is None:
            print(f'В данже {dungeon} нет {lvl} лвла')
            telegram.send_error_message(f'В данже {dungeon} нет {lvl} лвла', 'При попытке получить lvl_cords в go_to_dungeon')
            lvl_cords = all_lvls_cords.get(self.DEFAULT_LVL_TO_SEND)

        print('lvl cord is', lvl_cords)

        ahk.mouse_actions('move', x=dungeon_cords[0], y=dungeon_cords[1])
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1350, y=950)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=lvl_cords[0], y=lvl_cords[1])
        ahk.mouse_actions('click')

        time.sleep(5)

    def go_to_menu(self):
        """Фунция для перехода в меню"""
        ahk.mouse_actions('move', x=1775, y=80)
        ahk.mouse_actions('click')

    def go_to_dungeon_menu(self):
        """Функция для перехода в меню дажней"""
        ahk.mouse_actions('move', x=1600, y=460)
        ahk.mouse_actions('click')

    def wheel_dungeon_menu_down(self):
        """Фукнция для прокрутки меню с данжами вниз"""
        ahk.mouse_actions('move', x=600, y=500)
        for i in range(22):
            ahk.mouse_actions('wheel')

    def activate_autohunt(self):
        """Функция для активации автоохоты"""
        def __is_autohunt_enabled():
            """Функция для провкри включена ли автоохота"""
            image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_autohunt_enabled.png', area_of_screenshot=(1511, 545,
                                                                                                                  1512, 546))

            autohunt_colors = image.get_main_color(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\is_autohunt_enabled.png')

            print(f'autohunt_colors is {autohunt_colors}')

            if 250 <= autohunt_colors[0] <= 256 and 200 <= autohunt_colors[1] <= 220 and 150 <= autohunt_colors[2] <= 170:
                print('Автоохота включена')
                return True
            print('Автоохота не включена')
            return False

        if not __is_autohunt_enabled():
            ahk.mouse_actions('move', x=1525, y=555)
            ahk.mouse_actions('click')

    def tp_to_random_place_in_dungeon(self):
        """Фуцнкция которая нажимает кнопку рандомного тп в данже"""
        ahk.mouse_actions('move', x=200, y=250)
        ahk.mouse_actions('click')

        time.sleep(3)

        ahk.mouse_actions('move', x=1650, y=940)
        ahk.mouse_actions('click')

        time.sleep(3)

        ahk.mouse_actions('esc')

ingame = IngameActons()

class Init:
    """Класс для инициализации нужных переменных"""
    def __init__(self, path):
        global PATH_TO_DUNGEON_MASTER
        PATH_TO_DUNGEON_MASTER = path

    def get_accounts_and_dungeons_lvls(self):
        """Фуцнкция для получения словаря с лвлами данжей для аккаунтов"""
        if handler.is_file_available(f"{PATH_TO_DUNGEON_MASTER}dungeons_list_and_lvls_for_accounts.json"):
            with open(f"{PATH_TO_DUNGEON_MASTER}dungeons_list_and_lvls_for_accounts.json", "r", encoding='utf-8') as accs_and_dungeons:
                data = json.load(accs_and_dungeons)
                return data

    def get_accs_list(self):
        """Функция для получения списка аккаунтов"""
        if handler.is_file_available(f"{PATH_TO_DUNGEON_MASTER}dungeons_list_and_lvls_for_accounts.json"):
            with open(f"{PATH_TO_DUNGEON_MASTER}dungeons_list_and_lvls_for_accounts.json", "r", encoding='utf-8') as accs_list:
                data = json.load(accs_list)
                accs_dict = data.values()
                for i in accs_dict:
                    return i.keys()

class DungeonMasterMain:
    """Основной класс бота"""
    def __init__(self):
        self.DEFAULT_TIME_TO_WAIT_ACCOUNT_IN_DUNGEON = 3600

    def run(self):
        """Основная фуцния бота"""
        print(f'Дефолтное время ожидания аккаунта в данже {self.DEFAULT_TIME_TO_WAIT_ACCOUNT_IN_DUNGEON}\n'
              f'Путь до папки с ботом {PATH_TO_DUNGEON_MASTER}\n')


        for dungeon_name in dungeons.DUNGEON_NAMES:
            print(f'dungeon_name is {dungeon_name}')



        if not handler.is_account_name_valid(acc_name):
            lvl_to_send = ingame.DEFAULT_LVL_TO_SEND
        self._switch_dungeon('FRENZY_ISLAND', lvl_to_send)

    def _wait_for_hotkey_to_switch_dungeons(self):
        """Функция которая ожидает нажатия хоткея
        для переключения данжей"""
        pass

    def _switch_dungeon(self, dungeon, lvl):
        """Функция которая переключает данж на аккаунте"""
        ingame.go_to_menu()
        dungeon_menu_opened = False
        while dungeon_menu_opened is False:
            ingame.go_to_dungeon_menu()
            dungeon_menu_opened = handler.is_dungeon_menu_opened()

        ingame.go_to_dungeon(dungeon, lvl)

        ingame.activate_autohunt()

    def _get_dungeon_availiable_time(self, dungeon_num):
        """Функция которая смотрит доступное время в данже"""
        image.take_screenshot(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\available_time_in_dungeon.png', area_of_screenshot=(675, 360+(dungeon_num*110),
                                                                                                                    770, 400+(dungeon_num*110)))

        available_time = image.image_to_string(f'{PATH_TO_DUNGEON_MASTER}\\imgs\\available_time_in_dungeon.png', is_digits=False)

        if 'мин.' in available_time:
            available_time = available_time.replace('мин.', '').replace(' ', '')
            return available_time*60
        elif 'ч.' in available_time:
            available_time = available_time.replace('ч.', '').replace(' ', '')
            return available_time*120
        else:
            telegram.send_error_message_with_photo(f"{PATH_TO_DUNGEON_MASTER}\\imgs\\available_time_in_dungeon.png",
                                                   f'Не удалось получить доступное время данжа под номером {dungeon_num}\n'
                                                   f'Полученная строка: {available_time}',
                                                   'При получении available_time в _get_dungeon_availiable_time')
            return self.DEFAULT_TIME_TO_WAIT_ACCOUNT_IN_DUNGEON

    def __get_additional_availiable_time(self):
        """Функция для получения бонусного времени в данже"""
        pass
    def _wait_while_accounts_in_dungeons(self):
        """фунция которая ждет пока акки фармят в данже"""
        pass

def run(path):
    init = Init(path)
    global ACCOUNTS_AND_DUNGEONS_LVLS
    global ACCOUNTS_LIST
    ACCOUNTS_AND_DUNGEONS_LVLS = init.get_accounts_and_dungeons_lvls()
    ACCOUNTS_LIST = init.get_accs_list()



run(r'C:\Users\MIFIKUS\PycharmProjects\BigBot\DungeonMaster\\')
main = DungeonMasterMain()
time.sleep(5)
main.run('123')

#time.sleep(5)
#handler.is_dungeon_availiable(1)
#main._get_dungeon_availiable_time(2)
#ingame.go_to_dungeon('DEVASTATED_CASTLE',503)