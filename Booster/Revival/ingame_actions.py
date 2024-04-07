from Booster.MainClasses.classes import AHKActions

ahk = AHKActions()

def open_menu():
    ahk.move(1775, 80)
    ahk.click()

def open_revival_menu():
    ahk.move(1420, 450)
    ahk.click()

def switch_revival_class(class_num: int):
    ahk.move(80, 225 + (class_num * 90))
    ahk.click()

def click_revive_button():
    ahk.move(1400, 960)
    ahk.click()

def click_on_revive_lvl(x: int, y: int):
    ahk.move(x, y)
    ahk.click()
