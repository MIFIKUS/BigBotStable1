from CollectionMaster.classes import Image
import CollectionMaster.config.color_presets as color_presets
from CollectionMaster.config.set_path import set_path

PATH = set_path()

image = Image()

def check_if_filter_seted(num: int, is_half=False):
    x = 1740
    x1 = 1810

    y = 245 + (num * 80)
    y1 = y + 75

    if is_half:
        template_name = 'filter_is_selected_half.png'
    else:
        template_name = 'filter_is_selected.png'


    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_filter_seted.png',
                          area_of_screenshot=(x, y, x1, y1))

    is_filter_seted = image.matching(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_filter_seted.png',
                                     f'{PATH}\\imgs\\templates\\l2m_error_handler\\{template_name}')

    print(f'filter {num} status {is_filter_seted}')

    return is_filter_seted

def check_if_enough_scrolls():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_enough_scrolls.png',
                          area_of_screenshot=(890, 785, 891, 786))

    color = image.get_main_color(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_enough_scrolls.png')

    if color_presets.NOT_ENOUGH_SCROLLS_MIN_COLOR[0] <= color[0] <= color_presets.NOT_ENOUGH_SCROLLS_MAX_COLOR[0] and \
       color_presets.NOT_ENOUGH_SCROLLS_MIN_COLOR[1] <= color[1] <= color_presets.NOT_ENOUGH_SCROLLS_MAX_COLOR[1] and \
       color_presets.NOT_ENOUGH_SCROLLS_MIN_COLOR[2] <= color[2] <= color_presets.NOT_ENOUGH_SCROLLS_MAX_COLOR[2]:
        print('Not enough scrolls')
        return False
    print('Enough Scrolls')
    return True

def is_inventory_opened():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_inventory_opened.png',
                          area_of_screenshot=(1315, 170, 1410, 210))

    inventory_opened = image.matching(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_inventory_opened.png',
                                     f'{PATH}\\imgs\\templates\\l2m_error_handler\\inventory_opened.png')

    print(f'inventory_opened_status is {inventory_opened}')
    return inventory_opened

def is_modification_menu_opened():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_modification_menu_opened.png',
                          area_of_screenshot=(610, 165, 825, 215))

    menu_opened = image.matching(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_modification_menu_opened.png',
                                 f'{PATH}\\imgs\\templates\\l2m_error_handler\\modification_menu_opened.png',
                                 threshold=0.7)

    print(f'modification_opened_status is {menu_opened}')
    return menu_opened

def is_multimodification_menu_opened():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_multimodification_menu_opened.png',
                          area_of_screenshot=(735, 600, 1130, 640))

    menu_opened = image.matching(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_multimodification_menu_opened.png',
                                 f'{PATH}\\imgs\\templates\\l2m_error_handler\\multimodification_menu_opened.png',
                                  threshold=0.7)

    print(f'multimodification_opened_status is {menu_opened}')
    return menu_opened

def is_collection_menu_opened():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_collection_menu_opened.png',
                          area_of_screenshot=(1210, 65, 1472, 120))

    menu_opened = image.matching(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_collection_menu_opened.png',
                                 f'{PATH}\\imgs\\templates\\l2m_error_handler\\collection_menu_opened.png',
                                  threshold=0.7)

    print(f'collection_opened_status is {menu_opened}')
    return menu_opened

def is_choose_items_menu_opened():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_choose_item_menu_opened.png',
                          area_of_screenshot=(1565, 805, 1625, 855))

    menu_opened = image.matching(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_choose_item_menu_opened.png',
                                 f'{PATH}\\imgs\\templates\\l2m_error_handler\\choose_item_menu_opened.png',
                                  threshold=0.7)

    print(f'choose_item_opened_status is {menu_opened}')
    return menu_opened

def is_item_choosed():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_item_choosed.png',
                          area_of_screenshot=(1685, 810, 1725, 855))

    menu_opened = image.matching(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\is_item_choosed.png',
                                 f'{PATH}\\imgs\\templates\\l2m_error_handler\\item_choosed.png',
                                  threshold=0.7)

    print(f'item_choosed_status is {menu_opened}')
    return menu_opened

def need_to_agree_unsafe_sharp():
    image.take_screenshot(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\need_to_agree_unsafe_sharp.png',
                          area_of_screenshot=(1055, 690, 1056, 691))

    color = image.get_main_color(f'{PATH}\\imgs\\screenshots\\l2m_error_handler\\need_to_agree_unsafe_sharp.png')

    if color_presets.UNSAFE_SHARP_MIN_COLOR[0] <= color[0] <= color_presets.UNSAFE_SHARP_MAX_COLOR[0] and \
       color_presets.UNSAFE_SHARP_MIN_COLOR[1] <= color[1] <= color_presets.UNSAFE_SHARP_MAX_COLOR[1] and \
       color_presets.UNSAFE_SHARP_MIN_COLOR[2] <= color[2] <= color_presets.UNSAFE_SHARP_MAX_COLOR[2]:
        print('Need to agree unsafe sharp')
        return True
    print('Not need agree unsafe sharp')
    return False

