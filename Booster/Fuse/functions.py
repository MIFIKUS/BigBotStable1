from Booster.MainClasses.classes import Image, AHKActions, Windows
from Booster.Fuse import ingame_actions
from Booster.Fuse.tg import TGBot

import time

image = Image()
ahk = AHKActions()
windows = Windows()

tg = TGBot()


class FuseClasses:
    def make_fuse(self):
        ingame_actions.click_autochoise_button()

        if not self._is_fuse_availible():
            return False

        ingame_actions.start_fuse()
        time.sleep(1)
        while True:
            ingame_actions.show_fuse_result()

            if self._is_fuse_repeat_availible():
                ingame_actions.repeat_fuse()
            else:
                ingame_actions.exit_from_fuse()
                break

    def _is_fuse_availible(self):
        image.take_screenshot('Booster\\Fuse\\imgs\\screenshots\\is_fuse_availible.png', (1530, 430, 1531, 431))
        color = image.get_main_color('Booster\\Fuse\\imgs\\screenshots\\is_fuse_availible.png')

        print(f'is_fuse_availible: {color}')

        if 55 <= color[0] <= 110 and 60 <= color[1] <= 110 and 60 <= color[2] <= 120:
            return False
        return True

    def _is_fuse_repeat_availible(self):
        image.take_screenshot('Booster\\Fuse\\imgs\\screenshots\\is_repeat_availible.png', (930, 900, 1400, 1000))

        template_name = 'Booster\\Fuse\\imgs\\templates\\repeat_button.png'
        screenshot_name = 'Booster\\Fuse\\imgs\\screenshots\\is_repeat_availible.png'

        if image.matching(screenshot_name, template_name, threshold=0.6):
            print(f'Повторение фьза доступно')
            return True
        return False


class ConfirmMenu:

    def confirm(self, is_aghathion):
        card_name = self._get_card_name()
        acc_name = self._get_acc_name()

        if is_aghathion:
            tg.send_red_aghathion_message(card_name, acc_name)
        else:
            tg.send_red_class_message(card_name, acc_name)

        self._confirm_card()

    def _get_card_name(self):
        image.take_screenshot('Booster\\Fuse\\imgs\\screenshots\\card_name.png', (75, 280, 320, 320))
        card_name = image.image_to_string('Booster\\Fuse\\imgs\\screenshots\\card_name.png', False)

        return card_name

    def _confirm_card(self):
        ingame_actions.confirm_red_card()

    def _get_acc_name(self):
        return windows.get_acc_name()

    def need_to_confirm(self, is_aghathion: bool) -> bool:
        if not self._confirm_button_availible(is_aghathion):
            return False

        image.take_screenshot('Booster\\Fuse\\imgs\\screenshots\\need_to_confirm.png', (10, 200, 400, 600))

        template_path = 'Booster\\Fuse\\imgs\\templates\\empty_confirm_area.png'
        main_img_path = 'Booster\\Fuse\\imgs\\screenshots\\need_to_confirm.png'

        if image.matching(main_img_path, template_path):
            return False
        return True

    def _confirm_button_availible(self, is_aghathion: bool):
        if is_aghathion:
            image.take_screenshot('Booster\\Fuse\\imgs\\screenshots\\confirm_button_availible.png', (815, 130, 970, 220))
        else:
            image.take_screenshot('Booster\\Fuse\\imgs\\screenshots\\confirm_button_availible.png', (910, 135, 1125, 220))

        template_path = 'Booster\\Fuse\\imgs\\templates\\red_dot_confirm_button.png'
        main_img_path = 'Booster\\Fuse\\imgs\\screenshots\\confirm_button_availible.png'

        return image.matching(main_img_path, template_path)

