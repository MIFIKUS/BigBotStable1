import time

from CollectionMaster.classes import Windows, AHKActions, Image
from CollectionMaster.config import color_presets
from CollectionMaster.config.set_path import set_path

windows = Windows()
ahk = AHKActions()
image = Image()

PATH = set_path()

class CollectInfo:
    """Класс для сбора информации о предмете"""
    def __init__(self):
        self.color = self.identify_color()
        self.safe_sharp_lvl = self.identify_safe_sharp_lvl()
        self.ready_for_collection = self.check_if_ready_for_collection()
        self.there_is_collections = self.check_if_there_are_collections()
        self.equipped = self.check_if_equipped()
        #self.collection_sharp_lvl = self._get_collection_sharp_lvls_cords()

    def identify_color(self):
        """Метод для определения цвета шмотки"""
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\item_color.png', area_of_screenshot=(1500, 160, 1755, 225))

        color = image.get_main_color(f'{PATH}\\imgs\\screenshots\\item_color.png')

        print(color)

        if color_presets.WHITE_ITEM_MIN_COLOR[0] <= color[0] <= color_presets.WHITE_ITEM_MAX_COLOR[0] and \
           color_presets.WHITE_ITEM_MIN_COLOR[1] <= color[1] <= color_presets.WHITE_ITEM_MAX_COLOR[1] and \
           color_presets.WHITE_ITEM_MIN_COLOR[2] <= color[2] <= color_presets.WHITE_ITEM_MAX_COLOR[2]:
            return "WHITE"

        if color_presets.GREEN_ITEM_MIN_COLOR[0] <= color[0] <= color_presets.GREEN_ITEM_MAX_COLOR[0] and \
           color_presets.GREEN_ITEM_MIN_COLOR[1] <= color[1] <= color_presets.GREEN_ITEM_MAX_COLOR[1] and \
           color_presets.GREEN_ITEM_MIN_COLOR[2] <= color[2] <= color_presets.GREEN_ITEM_MAX_COLOR[2]:
            return "GREEN"

        elif color_presets.BLUE_ITEM_MIN_COLOR[0] <= color[0] <= color_presets.BLUE_ITEM_MAX_COLOR[0] and \
             color_presets.BLUE_ITEM_MIN_COLOR[1] <= color[1] <= color_presets.BLUE_ITEM_MAX_COLOR[1] and \
             color_presets.BLUE_ITEM_MIN_COLOR[2] <= color[2] <= color_presets.BLUE_ITEM_MAX_COLOR[2]:
            return "BLUE"

        elif color_presets.RED_ITEM_MIN_COLOR[0] <= color[0] <= color_presets.RED_ITEM_MAX_COLOR[0] and \
             color_presets.RED_ITEM_MIN_COLOR[1] <= color[1] <= color_presets.RED_ITEM_MAX_COLOR[1] and \
             color_presets.RED_ITEM_MIN_COLOR[2] <= color[2] <= color_presets.RED_ITEM_MAX_COLOR[2]:
            return "RED"

        else:
            return None

    def check_if_ready_for_collection(self):
        """Проверка можно ли прямо сейчас засунуть шмотку в колу"""
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\is_item_ready_for_collection.png', area_of_screenshot=(1406, 172, 1407, 173))

        color = image.get_main_color(f'{PATH}\\imgs\\screenshots\\is_item_ready_for_collection.png')

        print('item_name_color rgb', color)

        r_max = color_presets.COLLECTION_AVAILABLE_MAX_COLOR[0]
        g_max = color_presets.COLLECTION_AVAILABLE_MAX_COLOR[1]
        b_max = color_presets.COLLECTION_AVAILABLE_MAX_COLOR[2]

        r_min = color_presets.COLLECTION_AVAILABLE_MIN_COLOR[0]
        g_min = color_presets.COLLECTION_AVAILABLE_MIN_COLOR[1]
        b_min = color_presets.COLLECTION_AVAILABLE_MIN_COLOR[2]

        if r_min <= color[0] <= r_max and g_min <= color[1] <= g_max and b_min <= color[2] <= b_max:
            return True
        return False

    def check_if_there_are_collections(self):
        """Проверка на то есто ли колы со шмоткой"""
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\is_there_collection.png', area_of_screenshot=(1390, 160, 1420, 193))

        is_there_collection = image.matching(f'{PATH}\\imgs\\screenshots\\is_there_collection.png', f'{PATH}\\imgs\\templates\\collection_availiable.png')
        is_there_collection_1 = image.matching(f'{PATH}\\imgs\\screenshots\\is_there_collection.png', f'{PATH}\\imgs\\templates\\collection_availiable_1.png')

        if is_there_collection or is_there_collection_1:
            return True
        return False

    def check_if_equipped(self):
        """Проверка на то одета ли шмотка"""
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\is_equipped.png',
                              area_of_screenshot=(1390, 160, 1420, 193))

        equipped = image.matching(f'{PATH}\\imgs\\screenshots\\is_equipped.png', f'{PATH}\\imgs\\templates\\equipped.png')

        if equipped:
            return True
        return False

    def identify_safe_sharp_lvl(self):
        """Определение типа шмотки (оружие, броня и т.д.)"""
        image.take_screenshot(f'{PATH}\\imgs\\screenshots\\item_safe_sharp_lvl.png', area_of_screenshot=(1775, 220, 1800, 260))
        safe_sharp_lvl = image.image_to_string(f'{PATH}\\imgs\\screenshots\\item_safe_sharp_lvl.png', is_digits=True)
        try:
            safe_sharp_lvl = int(safe_sharp_lvl)
            return safe_sharp_lvl
        except ValueError:
            print('Не возможно перевести safe_sharp_lvl в int')
            print('safe_sharp_lvl', safe_sharp_lvl)
            return None

    def get_collection_sharp_lvls(self):
        pass
    def _get_collection_sharp_lvls_cords(self):
        def _move_mouse_to_item_area():
            ahk.move(1450, 450)

        _move_mouse_to_item_area()

        while image.matching(f'{PATH}\\imgs\\screenshots\\inventory\\item_area.png',
                             f'{PATH}\\imgs\\templates\\inventory\\modification_title.png',
                             True, 0.9, 0, (1380, 280, 1810, 650)) is False:

            ahk.drag(0, -150, True)
            _move_mouse_to_item_area()

            time.sleep(1)

        cords = image.matching(f'{PATH}\\imgs\\screenshots\\inventory\\item_area.png',
                             f'{PATH}\\imgs\\templates\\inventory\\modification_title.png',
                             True, 0.9, 1,  (1380, 280, 1810, 650))

        cords[0] += 1543
        cords[1] += 280

        print(f"Координаты надписи модификации найдены x = {cords[0]} y = {cords[1]}")

        return cords


if __name__ == '__main__':
    time.sleep(5)
    c = CollectInfo()

    print('color', c.color)
    print('safe_sharp_lvl', c.safe_sharp_lvl)
    print('ready for collection', c.ready_for_collection)
    print('is there collections', c.there_is_collections)
    print('is equipped', c.equipped)
