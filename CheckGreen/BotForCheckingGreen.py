from ahk import AHK
import cv2
import numpy as np
import pyscreenshot
import time
import random
import keyboard

import psutil
from PIL import Image


#как ты в видосе объяснял эти пресеты
PRESET = 1

MULTIPLIER = 1

HOTKEY = 'ctrl+f1'

autohotkey = AHK()

class AHKActions():
    # Переменная action отвечает за то, какое действие нужно сделать. (кликнуть, перевести мышку, провести мышкой с нажатием)
    def mouse_actions(self, action, x=0, y=0, direction='R', text=''):
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
        elif action == 'type':
            while True:
                if autohotkey.type(text) is not False:
                    break

        for proc in psutil.process_iter():
            if proc.name() == 'AutoHotkey.exe':
                proc.kill()
ahk = AHKActions()

class ImageWork():

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

    def get_main_color(self, file):
        img = Image.open(file)
        colors = img.getcolors(256)  # put a higher value if there are many colors in your image
        max_occurence, most_present = 0, 0
        try:
            for c in colors:
                if c[0] > max_occurence:
                    (max_occurence, most_present) = c
            return most_present
        except TypeError:
            raise Exception("Too many colors in the image")

ahk = AHKActions()

image_work = ImageWork()


class InGame():
    def check_green_on_image(self):

         time.sleep(0.5*MULTIPLIER)
         image_work.take_screenshot('card_1.png', area_of_screenshot=(1133, 320, 1345, 350))
         card_color = image_work.get_main_color('card_1.png')
         print(card_color)
         if card_color != (0, 30, 10):
             return False
         if PRESET > 1:
             time.sleep(0.5*MULTIPLIER)
             image_work.take_screenshot('card_2.png', area_of_screenshot=(890, 725, 1102, 775))
             card_color = image_work.get_main_color('card_2.png')
             print(card_color)
             if card_color != (1, 63, 29):
                 return False
             if PRESET > 2:
                 time.sleep(0.5*MULTIPLIER)
                 image_work.take_screenshot('card_3.png', area_of_screenshot=(1133, 540, 1345, 590))
                 card_color = image_work.get_main_color('card_3.png')
                 print(card_color)
                 if card_color != (1, 63, 29):
                     return False
                 if PRESET > 3:
                     time.sleep(0.5*MULTIPLIER)
                     image_work.take_screenshot('card_4.png', area_of_screenshot=(430, 723, 642, 773))
                     card_color = image_work.get_main_color('card_4.png')
                     print(card_color)
                     if card_color != (1, 63, 29):
                         return False
         return True


ingame = InGame()

def main():
    while ingame.check_green_on_image() is False:
        ahk.mouse_actions('y')
        ahk.mouse_actions('move', x=1080, y=700)
        ahk.mouse_actions('click')
        time.sleep(1.5*MULTIPLIER)

def run(hotkey, mode, multiplier):
    global MULTIPLIER

    global PRESET
    MULTIPLIER = int(multiplier)

    PRESET = int(mode)
    keyboard.add_hotkey(HOTKEY, main)
    keyboard.wait()
    print('Все готово!')

