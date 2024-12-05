from Booster.MainClasses.classes import Image, AHKActions
import time

image = Image()
ahk = AHKActions()


def accept_fuse():
    ahk.move(1050, 700)
    ahk.click()

def skip_fuse():
    for _ in range(10):
        ahk.move(900, 960)
        ahk.click()
        time.sleep(0.5)
    time.sleep(10)

def get_fuse_percents():
    def _clear_percents_string(text):
        print(text)
        text = text.replace(' ', '')
        text = text.replace('\n', '')

        try:
            text = text.split('%')[0]
            return text
        except Exception as e:
            return False

    image.take_screenshot('Booster\\Souls\\imgs\\screenshots\\fuse_percents.png', (330, 657, 650, 702))
    image.delete_all_colors_except_one('Booster\\Souls\\imgs\\screenshots\\fuse_percents.png', [250, 250, 250], [255, 255, 255])

    fuse_percents = image.image_to_string('Booster\\Souls\\imgs\\screenshots\\fuse_percents.png', True)

    fuse_percents = _clear_percents_string(fuse_percents)
    if fuse_percents is False:
        return 0

    try:
        print(fuse_percents)
        return float(fuse_percents)

    except Exception as e:
        print(e)
        return False

def is_fuse_availible():
    image.take_screenshot('Booster\\Souls\\imgs\\screenshots\\is_fuse_availible.png', (1000, 940, 1001, 941))
    color = image.get_main_color('Booster\\Souls\\imgs\\screenshots\\is_fuse_availible.png')

    if 95 <= color[0] <= 115 and 40 <= color[1] <= 65 and 0 <= color[2] <= 20:
        return False
    return True


def menu_opened() -> bool:
    image.take_screenshot('is_menu_opened.png', (1730, 180, 1820, 292))
    return image.matching('is_menu_opened.png', 'menu_opened.png')
