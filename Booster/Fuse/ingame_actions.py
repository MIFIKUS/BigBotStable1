from Booster.MainClasses.classes import AHKActions
import time


ahk = AHKActions()
def open_menu():
    ahk.move(1770, 80)
    ahk.click()

def open_classes_menu():
    ahk.move(1340, 220)
    ahk.click()

def open_aghathions_menu():
    ahk.move(1430, 220)
    ahk.click()

def open_fusion_menu():
    ahk.move(780, 190)
    ahk.click()

def open_fusion_menu_aghathion():
    ahk.move(400, 200)
    ahk.click()

def click_autochoise_button():
    ahk.move(930, 950)
    ahk.click()

def start_fuse():
    ahk.move(1400, 960)
    ahk.click()

def show_fuse_result():
    ahk.move(950, 950)
    ahk.click()

def repeat_fuse():
    ahk.move(980, 950)
    ahk.click()

def reset_fuse_menu():
    time.sleep(2)

    ahk.move(340, 190)
    ahk.click()

    open_fusion_menu()

def reset_fuse_menu_aghathion():
    time.sleep(2)

    ahk.move(140, 190)
    ahk.click()

    open_fusion_menu_aghathion()

def exit_from_fuse():
    ahk.move(900, 950)
    ahk.click()

def open_confirm_red_menu():
    ahk.move(1200, 190)
    ahk.click()

def open_confirm_red_menu_aghathion():
    ahk.move(840, 190)
    ahk.click()

def confirm_red_card():
    ahk.move(200, 870)
    ahk.click()

    ahk.move(960, 700)
    ahk.click()

