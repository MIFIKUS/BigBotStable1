from Booster.MainClasses.classes import AHKActions

ahk = AHKActions()


def open_menu():
    ahk.move(1770, 80)
    ahk.click()

def open_stamps_menu():
    ahk.move(1515, 330)
    ahk.click()

def go_next_stamp(num_of_stamp: int):
    ahk.move(75, 220+(num_of_stamp * 80))
    ahk.click()

def impress_stamp():
    ahk.move(1400, 960)
    ahk.click()

def reset_impress_menu():
    ahk.move(230, 950)
    ahk.click()
