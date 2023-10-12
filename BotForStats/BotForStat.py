from ahk import AHK

import cv2
import numpy as np
import pyscreenshot
import pytesseract
import time
import random
import keyboard
import psutil


#как ты в видосе объяснял эти пресеты
PRESET = 1

MULTIPLIER = 1

HOTKEY = 'ctrl+f2'


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
autohotkey = AHK()

class AHKActions():
    # Переменная action отвечает за то, какое действие нужно сделать. (кликнуть, перевести мышку, провести мышкой с нажатием)
    def mouse_actions(self, action, x=0, y=0):

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
            autohotkey.key_press('y')
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
ahk = AHKActions()

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
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789+%')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 3')
        return text


STAT_DICT = {'макс. нр': '+10', 'макс. грузоподъемность': '+40', 'мдр': '+1'}

image = Image()
class InGame():




    def find_current_stats(self):
        area_of_screenshot_for_stat = [630, 500, 1150, 535]
        area_of_screenshot_for_stat_value = [1190, 500, 1240, 535]

        dict_of_stats_and_values = {}
        for i in range(len(STAT_DICT.items())):
            image.take_screenshot(f'stat_{i}.png', area_of_screenshot_for_stat)
            image.take_screenshot(f'value_{i}.png', area_of_screenshot_for_stat_value)

            stat = image.image_to_string(f'stat_{i}.png', is_digits=False).lower().replace('\n', '')
            value = image.image_to_string(f'value_{i}.png', is_digits=True).lower().replace('\n', '')

            area_of_screenshot_for_stat[1] += 40
            area_of_screenshot_for_stat[3] += 40

            area_of_screenshot_for_stat_value[1] += 40
            area_of_screenshot_for_stat_value[3] += 40

            dict_of_stats_and_values[stat] = value

        return dict_of_stats_and_values.items()

    def compare_current_stats_and_neccesary(self):
        current_stats = self.find_current_stats()
        print(list(current_stats))
        print(list(STAT_DICT.items()))
        stat_dict = STAT_DICT.items()
        print(current_stats)
        for i in range(len(stat_dict)):
            if 'ничего' in list(stat_dict)[i][0]:
                print('STAT', i+1, 'GOOD')
            elif 'ничего' in list(stat_dict)[i][1]:
                if list(current_stats)[i][0] == list(stat_dict)[i][0]:
                    print('STAT', i+1, 'GOOD')
                else:
                    print('STAT', i+1, 'BAD')
                    return False
            elif list(current_stats)[i] == list(stat_dict)[i]:
                print('STAT', i+1, 'GOOD')
            else:
                print('STAT', i+1, 'BAD')
                return False
        return True

ingame = InGame()



def main():
    while True:
        try:
            if ingame.compare_current_stats_and_neccesary() is False:
                ahk.mouse_actions('y')
                time.sleep(3)
            else:
                break
        except:
            print('Два одинаковый стата')
            continue
def run(statlist, multiplier):
    global STAT_DICT
    global MULTIPLIER

    STAT_DICT = eval(statlist.lower())
    MULTIPLIER = float(multiplier)

    keyboard.add_hotkey(HOTKEY, main)
    keyboard.wait()




