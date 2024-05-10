from difflib import SequenceMatcher
from PIL import Image as pil

import PIL.ImageGrab
import numpy as np
import cv2
import pytesseract
import re
import time


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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

    def get_main_color(self, file, colors_amount=1024):
        img = pil.open(file)
        colors = img.getcolors(colors_amount)
        colors = sorted(colors)
        if (0,0,0) in colors:
           colors.remove(colors[0])
        return colors[0][1]

    def menu_opened(self):
        time.sleep(0.1)
        return self.matching('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_menu_opened.png',
                         'jwt_updater\\l2m_actions\\imgs\\templates\\menu_opened.png',
                         True, area_of_screenshot=(1720, 170, 1825, 300))

    def market_opened(self):
        time.sleep(0.1)
        return self.matching('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_market_opened.png',
                         'jwt_updater\\l2m_actions\\imgs\\templates\\market_opened.png',
                         True, area_of_screenshot=(1550, 60, 1750, 130))

    def globaL_market_opened(self):
        self.take_screenshot('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_global_market_open.png', area_of_screenshot=(1335, 90, 1336, 91))
        color = self.get_main_color('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_global_market_open.png')
        print(color)
        if not (250 < color[0] < 256) and not (250 < color[1] < 256) and not (250 < color[2] < 256):
            return False
        else:
            return True

    def search_area_opened(self):
        time.sleep(0.1)
        return self.matching('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_search_area_opened.png',
                             'jwt_updater\\l2m_actions\\imgs\\templates\\search_area_opened.png',
                             True, area_of_screenshot=(1345, 150, 1600, 245))

    def settings_opened(self):
        time.sleep(0.1)
        return self.matching('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_settings_opened.png',
                             'jwt_updater\\l2m_actions\\imgs\\templates\\settings_opened.png',
                             True, area_of_screenshot=(1485, 65, 1740, 130))

    def information_opened(self):
        time.sleep(0.1)
        return self.matching('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_information_opened.png',
                             'jwt_updater\\l2m_actions\\imgs\\templates\\information_opened.png',
                             True, area_of_screenshot=(795, 905, 1060, 990))

    def all_categories_opened(self):
        time.sleep(0.1)
        self.take_screenshot('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_market_open.png', area_of_screenshot=(50, 377, 51, 379))
        color = self.get_main_color('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_market_open.png')
        print(color)
        if not (250 < color[0] < 256) and not (250 < color[1] < 256) and not (250 < color[2] < 256):
            return False
        else:
            return True

    def get_price(self) -> bool or int:
        def _check_if_no_item():
            return self.matching('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_no_item.png',
                                 'jwt_updater\\l2m_actions\\imgs\\templates\\no_item.png',
                                 True, area_of_screenshot=(1105, 440, 1135, 480))
        while True:
            self.take_screenshot('jwt_updater\\l2m_actions\\imgs\\screenshots\\price.png', (1110, 445, 1210, 490))
            price = self.image_to_string('jwt_updater\\l2m_actions\\imgs\\screenshots\\price.png', True)
            price = price.replace('\n', '')
            price = price.replace(' ', '')

            if price:
                try:
                    return int(price)
                except:
                    print('Не удалось получить цену')

            else:
                if _check_if_no_item():
                    return False

    def get_server(self):
        SERVERS = ['леона', 'эрика', 'зигхард', 'барц']

        self.take_screenshot('jwt_updater\\l2m_actions\\imgs\\screenshots\\server.png', (1200, 450,
                                                                                                                      1430, 480))

        server_name = self.image_to_string('jwt_updater\\l2m_actions\\imgs\\screenshots\\server.png', False)

        server_name = re.sub(r'[^а-яА-Яa-zA-Z]', '', server_name).lower()

        for i in SERVERS:
            if SequenceMatcher(a=i, b=server_name).ratio() >= 0.9:
                return i

    def get_cheapest_sharp(self, price: int) -> int:
        while True:
            self.take_screenshot('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_cheapest_sharp.png', (1110, 445,
                                                                                                                                     1220, 475))

            current_price = self.image_to_string('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_cheapest_sharp.png',
                                                 True)
            current_price = current_price.replace('\n', '')
            current_price = current_price.replace(' ', '')

            try:
                int(current_price)
                break
            except Exception as e:
                print(f'Не удалось получить цену {e}')

        for i in range(4):
            y_cords = 445 + (120 * i)
            self.take_screenshot('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_cheapest_sharp.png', (1110, y_cords,
                                                                                                                                     1220, y_cords + 30))

            current_price = self.image_to_string('jwt_updater\\l2m_actions\\imgs\\screenshots\\is_cheapest_sharp.png', True)
            current_price = current_price.replace('\n', '')
            current_price = current_price.replace(' ', '')

            try:
                int(current_price)
            except Exception as e:
                print(f'Не удалось получить цену {e}')
                return False

            if int(current_price) == price:
                return i
        return False

    def get_price_in_final_menu(self, price: int) -> bool:
        self.take_screenshot('jwt_updater\\l2m_actions\\imgs\\screenshots\\final_price.png', (1625, 455, 1740, 485))
        current_price = self.image_to_string('jwt_updater\\l2m_actions\\imgs\\screenshots\\final_price.png', True)
        current_price = current_price.replace('\n', '')
        current_price = current_price.replace(' ', '')

        try:
            int(current_price)
        except Exception as e:
            print(f'Не удалось получить цену {e}')
            return False

        if current_price == price:
            return True

