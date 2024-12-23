from Booster.MainClasses.classes import Image


image = Image()


def craft_available() -> bool:
    image.take_screenshot('Booster\\Scrolls\\imgs\\screenshots\\is_craft_available.png', (1570, 920, 1571, 921))
    color = image.get_main_color('Booster\\Scrolls\\imgs\\screenshots\\is_craft_available.png')

    if 95 <= color[0] <= 115 and 40 <= color[1] <= 60 and 0 <= color[2] <= 15:
        return False
    return True


def menu_opened() -> bool:
   image.take_screenshot('is_menu_opened.png', (1730, 180, 1820, 292))
   return image.matching('is_menu_opened.png', 'menu_opened.png')
