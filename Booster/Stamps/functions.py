from Booster.MainClasses.classes import AHKActions, Image
from Booster.Stamps import ingame_actions
import time


ahk = AHKActions()
image = Image()


class ImpressStamps:
    def __init__(self):
        self.MAX_IMPRESS_LVL = 5

    def impress(self):
        while True:
            impress_lvl = self._get_impress_lvl()
            if impress_lvl is False:
                return
            if impress_lvl == self.MAX_IMPRESS_LVL:
                return

            ingame_actions.impress_stamp()
            time.sleep(2)

            if self._impress_availible():
                ingame_actions.impress_stamp()
                time.sleep(2)
            else:
                return False

            ingame_actions.reset_impress_menu()
            time.sleep(2)


    def _get_impress_lvl(self):
        image.take_screenshot('Booster\\Stamps\\imgs\\screenshots\\impress_lvl.png', (350, 335, 440, 410))

        lvls = {
            3: 'Booster\\Stamps\\imgs\\templates\\three_lvl.png',
            2: 'Booster\\Stamps\\imgs\\templates\\two_lvl.png',
            1: 'Booster\\Stamps\\imgs\\templates\\one_lvl.png',
            4: 'Booster\\Stamps\\imgs\\templates\\four_lvl.png',
            5: 'Booster\\Stamps\\imgs\\templates\\five_lvl.png',
            6: 'Booster\\Stamps\\imgs\\templates\\six_lvl.png'}

        for lvl, img_path in lvls.items():
            is_match = image.matching('Booster\\Stamps\\imgs\\screenshots\\impress_lvl.png', img_path)

            if is_match:
                return lvl
        return False

    def _impress_availible(self):
        image.take_screenshot('Booster\\Stamps\\imgs\\screenshots\\impress_availible.png', (1450, 930, 1451, 931))

        color = image.get_main_color('Booster\\Stamps\\imgs\\screenshots\\impress_availible.png')

        if 95 <= color[0] <= 115 and 40 <= color[1] <= 60 and 0 <= color[2] <= 15:
            return False
        return True

    def menu_opened(self) -> bool:
        image.take_screenshot('is_menu_opened.png', (1730, 180, 1820, 292))
        return image.matching('is_menu_opened.png', 'menu_opened.png')
