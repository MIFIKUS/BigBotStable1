from ahk import AHK

import pyscreenshot
import pytesseract
import numpy as np
import cv2

import win32gui
import win32com.client
import win32con

import json
import random
import time

import gspread
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
autohotkey = AHK()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

new_statistics = {}

class GoogleSheets():
    def write_labels(self):
        SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1qwPa93plt7a_ArFfi05tQZ3pl5o1BSfcIet9GtePkFo/edit#gid=0"
        gs = gspread.service_account('credential_for_statistics.json')
        sh = gs.open_by_url(SPREADSHEET_URL)
        ws = sh.sheet1
        LABELS = ['Аккаунт', 'Баланс', 'Баланс на ауке', 'Продано шмоток', 'Доход с продаж', 'Слоты', 'Сервер']
        ws.append_row(LABELS)


    def write_google(self, data):
        SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1qwPa93plt7a_ArFfi05tQZ3pl5o1BSfcIet9GtePkFo/edit#gid=0"
        gs = gspread.service_account('credential_for_statistics.json')
        sh = gs.open_by_url(SPREADSHEET_URL)
        ws = sh.sheet1
        ws.append_row(data)


    def clear_google(self):
        SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1qwPa93plt7a_ArFfi05tQZ3pl5o1BSfcIet9GtePkFo/edit#gid=0"
        gs = gspread.service_account('credential_for_statistics.json')
        sh = gs.open_by_url(SPREADSHEET_URL)
        ws = sh.sheet1
        ws.clear()

class AHKActions():

    # Переменная action отвечает за то, какое действие нужно сделать. (кликнуть, перевести мышку, провести мышкой с нажатием)
    def mouse_actions(self, action, x=0, y=0):

        if action == 'move':
            move = f'''\
            CoordMode, Mouse, Screen  ;
            MouseMove, {x}, {y}, 0
            '''
            try:
                while autohotkey.get_mouse_position(coord_mode='Screen') != (x, y):
                    autohotkey.run_script(move)
                    time.sleep(0.5)
            except:
                pass

            return

        elif action == 'click':
            click = '''\
                SendEvent {Click}
                '''
            try:
                autohotkey.run_script(click)
                time.sleep(0.5)
            except:
                pass

            return

        elif action == 'drag':
            drag = f'''\
            Click down
            Sleep, 120
            MouseMove, {x}, {y}, 3, R
            Sleep, 120
            Click
            '''
            try:
                autohotkey.run_script(drag)
            except:
                pass
            time.sleep(1)
            return


        elif action == 'wheel':
            wheel = f'''\
            MouseClick,WheelDown,,,1,0,D,R
            '''
            autohotkey.run_script(wheel)
            return

        elif action == 'esc':
            esc = '''\
            SendInput, {Esc}
            '''
            autohotkey.run_script(esc)
            return

        elif action == 'y':
            y = '''\
            SendInput, {y}
            '''
            autohotkey.run_script(y)
            return

        elif action == 'press':
            click_down = '''\
            Click down
            '''

            click_up = '''\
            Click up
            '''

            try:
                autohotkey.run_script(click_down)
            except:
                pass
            time.sleep(2)
            try:
                autohotkey.run_script(click_up)
            except:
                pass
            return


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

    def image_to_string(self, image_name, is_digits):


        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789/')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 3')
        return text



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

                win32gui.ShowWindow(window, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(window)
                for i in range(2):
                    if self.is_screen_locked() is True:
                        self.unlock_screen()
                if self._is_dead() is True:
                    self._revive()
                    time.sleep(5)
                func(window)



    def _is_dead(self):
        image.take_screenshot('main_screen.jpg')
        if image.matching('main_screen.jpg', 'dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching('main_screen.jpg', 'dead2.png', need_for_taking_screenshot=True) is True:
            return True

    def _revive(self):
        ahk.mouse_actions('move', x=900, y=870)
        ahk.mouse_actions('click')

    def is_screen_locked(self):
        for i in range(2):
            is_locked = image.matching('main_screen.jpg', 'screen_is_locked.png', need_for_taking_screenshot=True)
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

window = Windows()
google = GoogleSheets()

def update_statistics(hwnd):
    ahk.mouse_actions('move', x=1775, y=85)
    ahk.mouse_actions('click')

    ahk.mouse_actions('move', x=1680, y=330)
    ahk.mouse_actions('click')

    ahk.mouse_actions('move', x=700, y=185)
    ahk.mouse_actions('click')

    image.take_screenshot('balance.png', area_of_screenshot=(840, 65, 908, 100))
    image.take_screenshot('sold_items.png', area_of_screenshot=(160, 960, 245, 1000))
    image.take_screenshot('income.png', area_of_screenshot=(1450, 960, 1520, 1000))

    acc_name = win32gui.GetWindowText(hwnd)
    acc_name = acc_name.replace('Lineage2M l ', '')

    ahk.mouse_actions('move', x=400, y=190)
    ahk.mouse_actions('click')

    image.take_screenshot('amount_on_market.png', area_of_screenshot=(150, 930, 235, 980))
    image.take_screenshot('balance_on_market.png', area_of_screenshot=(400, 935, 520, 985))

    ahk.mouse_actions('esc')
    time.sleep(0.2)


    ahk.mouse_actions('move', x=1775, y=80)
    ahk.mouse_actions('click')

    ahk.mouse_actions('move', x=1680, y=720)
    ahk.mouse_actions('click')
    time.sleep(0.2)

    ahk.mouse_actions('move', x=1600, y=180)
    ahk.mouse_actions('click')
    time.sleep(0.2)

    image.take_screenshot('server.png', area_of_screenshot=(1250, 445, 1430, 490))

    balance = image.image_to_string('balance.png', is_digits=True)
    sold_items = image.image_to_string('sold_items.png', is_digits=True)
    income = image.image_to_string('income.png', is_digits=True)
    amount_on_market = image.image_to_string('amount_on_market.png', is_digits=True)
    balance_on_market = image.image_to_string('balance_on_market.png', is_digits=True)
    server = image.image_to_string('server.png', is_digits=False)

    new_statistics[acc_name] = {"Баланс на акке": balance, "Продано шмоток": sold_items, "Общий доход с продаж": income,
                                "Баланс на ауке":balance_on_market, "кол-во шмоток в ауке": amount_on_market}
    ahk.mouse_actions('esc')
    window.lock_screen()

    google.write_google([acc_name, balance, balance_on_market, sold_items, income, amount_on_market, server])

    print(new_statistics)



    with open('statistics.json', 'w', encoding='utf-8') as statistics_json:
        json.dump(new_statistics, statistics_json,ensure_ascii=False)





def run():
    pass
    #CREDENTIALS_FILE = 'credential_for_statistics.json'  # Имя файла с закрытым ключом, вы должны подставить свое
#
    ## Читаем ключи из файла
    #credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
#
    #httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    #service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
#
    #driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    #access = driveService.permissions().create(
    #    fileId = '1qwPa93plt7a_ArFfi05tQZ3pl5o1BSfcIet9GtePkFo',
    #    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'alchoholru.2.4.5@gmail.com'},  # Открываем доступ на редактирование
    #    fields = 'id'
    #).execute()

    #google.write_labels()
    #window.switch_windows(update_statistics)
#SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1lICdsTXnU4COlW1Bwj7A3rTOVFyBHs9UX__uiXmaDGE"
#gs = gspread.service_account('credential_for_statistics.json')
#sh = gs.open_by_url(SPREADSHEET_URL)
#sh.share('kedrindaniil@gmail.com', perm_type='user', role='writer')







