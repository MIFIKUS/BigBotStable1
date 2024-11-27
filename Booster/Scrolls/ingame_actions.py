from Booster.MainClasses.classes import AHKActions

ahk = AHKActions()


def open_menu():
    ahk.move(1780, 90)
    ahk.click()


def open_craft_menu():
    ahk.move(1500, 460)
    ahk.click()


def choose_other():
    ahk.move(1040, 200)
    ahk.click()


def open_gods_orders():
    ahk.move(100, 830)
    ahk.click()


def choose_order_signs():
    ahk.move(340, 460)
    ahk.click()


def click_on_oder_sign():
    ahk.move(340, 270)
    ahk.click()


def set_max_amount():
    ahk.move(1050, 940)
    ahk.click()


def craft():
    ahk.move(1550, 950)
    ahk.click()


def skip_craft():
    ahk.move(1010, 940)
    ahk.click()


def exit_from_craft_menu():
    ahk.move(1800, 90)
    ahk.click()
