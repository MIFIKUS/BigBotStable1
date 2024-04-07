from Booster.MainClasses.classes import AHKActions

ahk = AHKActions()


def open_inventory():
    ahk.move(1550, 80)
    ahk.click()

def close_inventory():
    ahk.move(1785, 175)
    ahk.click()

def open_grocery():
    ahk.move(1340, 445)
    ahk.click()

def open_filter_menu():
    ahk.move(1340, 730)
    ahk.click()

def close_filter_menu():
    ahk.move(1340, 730)
    ahk.click()

def switch_all():
    ahk.move(1700, 270)
    ahk.click()

def switch_cases():
    ahk.move(1700, 440)
    ahk.click()

def open_case(x, y):
    ahk.move(x, y)
    for _ in range(2):
        ahk.click()

def toggle_autouse(x, y):
    ahk.move(x, y)
    ahk.click()

    ahk.drag(0, 50, True)

def set_max_clock_menu():
    ahk.move(1000, 630)
    ahk.click()

def choose_clock():
    ahk.move(730, 480)
    ahk.click()

def agree_clock_choose():
    ahk.move(1000, 740)
    ahk.click()

def choose_red_accesory_receipt():
    ahk.move(1040, 480)
    ahk.click()

def set_max_red_accesory_menu():
    ahk.move(1000, 630)
    ahk.click()

def agree_red_receipt_choose():
    ahk.move(1000, 740)
    ahk.click()

