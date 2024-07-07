def is_dead(self):
    """Проверка на то, умер ли персонаж"""

    image.take_screenshot(f'{PATH_TO_ALCHEMY}\\imgs\\is_dead.png', area_of_screenshot=(730, 825, 1125, 920))

    dead_button_1 = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_dead.png',
                                   f'{PATH_TO_ALCHEMY}\\imgs\\dead.png', need_for_taking_screenshot=False)

    dead_button_2 = image.matching(f'{PATH_TO_ALCHEMY}\\imgs\\is_dead.png',
                                   f'{PATH_TO_ALCHEMY}\\imgs\\dead2.png', need_for_taking_screenshot=False)

    if dead_button_1 or dead_button_2:
        time.sleep(10)
        self._revive()
        return True
    return False