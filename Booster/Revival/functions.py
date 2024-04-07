from Booster.MainClasses.classes import AHKActions, Image
from Booster.Revival import ingame_actions
import time

ahk = AHKActions()
image = Image()

class Revive:
    def revive(self):
        ingame_actions.click_revive_button()
        time.sleep(3)

        while self._revival_going():
            ingame_actions.click_revive_button()
            time.sleep(12)
            if not self.revive_availible():
                for _ in range(2):
                    ahk.esc()
                break

    def _revival_going(self):
        image.take_screenshot('Booster\\Revival\\imgs\\screenshots\\is_revival_going.png', (40, 900, 345, 1000))

        main_img_path = 'Booster\\Revival\\imgs\\screenshots\\is_revival_going.png'
        template_img_path = 'Booster\\Revival\\imgs\\templates\\revival_going.png'

        return image.matching(main_img_path, template_img_path)

    def revive_availible(self) -> bool:
        image.take_screenshot('Booster\\Revival\\imgs\\screenshots\\is_revive_availible.png', (1435, 935, 1436, 936))
        color = image.get_main_color('Booster\\Revival\\imgs\\screenshots\\is_revive_availible.png')

        if 85 <= color[0] <= 125 and 30 <= color[1] <= 70 and 0 <= color[2] <= 25:
            return False
        return True


class AccActions:
    def get_balance(self) -> int:
        start_cords = self._get_balance_cords()

        if start_cords is False:
            return 0

        image.take_screenshot('Booster\\Revival\\imgs\\screenshots\\balance.png', (start_cords[0], 65, start_cords[0]+200, 100))
        image.delete_all_colors_except_one('Booster\\Revival\\imgs\\screenshots\\balance.png', [250, 250, 250], [255, 255, 255])

        balance = image.image_to_string_comma('Booster\\Revival\\imgs\\screenshots\\balance.png')
        balance = ''.join(filter(str.isdigit, balance))

        try:
            balance = int(balance)
            return balance
        except Exception as e:
            print(e)
            return 0

    def _get_balance_cords(self) -> list:
        image.take_screenshot('Booster\\Revival\\imgs\\screenshots\\revival_balance_area.png', (1100, 55, 1385, 110))

        main_img_path = 'Booster\\Revival\\imgs\\screenshots\\revival_balance_area.png'
        template_img_path = 'Booster\\Revival\\imgs\\templates\\revival_balance_logo.png'

        cords = image.matching(main_img_path, template_img_path, func=1)

        if cords is False:
            print(f'Не удалось получить коордианты')
        else:
            cords[0] += 1093
            print(f'Удалось получить координаты лого с баликом x: {cords[0]} y:{cords[1]}')

        return cords
    

