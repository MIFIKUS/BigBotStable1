from Booster.MainClasses.classes import Image

image = Image()


class Checks:
    def check_all_switch(self):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\all_switch.png', (1755, 255, 1805, 310))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\all_switch.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\switch_on.png'

        return image.matching(main_img_name, template_img_name)

    def check_cases_switch(self):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\cases_switch.png', (1755, 410, 1805, 465))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\cases_switch.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\switch_on.png'

        return image.matching(main_img_name, template_img_name)

    def check_if_case_is_apple(self, slot):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\case.png', (1385+(slot*102), 235,
                                                                                                           1495+(slot*102), 345))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\case.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\apple_case.png'

        return image.matching(main_img_name, template_img_name)

    def check_if_case_is_book(self, slot):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\case.png', (1385+(slot*102), 235,
                                                                                                           1495+(slot*102), 345))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\case.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\book_case.png'

        return image.matching(main_img_name, template_img_name)

    def check_if_case_is_skip(self, slot):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\case.png', (1385+(slot*102), 235,
                                                                                                           1495+(slot*102), 345))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\case.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\skip_case.png'

        return image.matching(main_img_name, template_img_name, threshold=0.7)

    def check_if_nomore_cases(self, slot):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\is_nomore_cases.png', (1385+(slot*102), 235,
                                                                                                                      1500+(slot*102), 345))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\is_nomore_cases.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\nomore_cases.png'

        return image.matching(main_img_name, template_img_name)

    def clock_menu_open(self):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\is_clock_menu_open.png', (615, 280, 1250, 810))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\is_clock_menu_open.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\clocks_menu.png'

        return image.matching(main_img_name, template_img_name)

    def red_recipe_open(self):
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\is_red_recipe_menu_open.png', (615, 280, 1250, 810))

        main_img_name = 'Booster\\Cases\\imgs\\screenshots\\is_red_recipe_menu_open.png'
        template_img_name = 'Booster\\Cases\\imgs\\templates\\red_recipe_menu.png'

        result = image.matching(main_img_name, template_img_name)
        if result is False:
            return image.matching(main_img_name, 'Booster\\Cases\\imgs\\templates\\red_recipe_menu_1.png')

        return result

    def enough_slots_in_inventory(self) -> bool:
        image.take_screenshot('Booster\\Cases\\imgs\\screenshots\\amounts_of_slots.png', (1310, 290, 1390, 322))

        slots = image.image_to_string('Booster\\Cases\\imgs\\screenshots\\amounts_of_slots.png', True).split('/')

        return True if int(slots[0]) != int(slots[1]) else False



