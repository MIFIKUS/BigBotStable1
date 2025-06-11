from Booster.MainClasses.classes import AHKActions
import time

ahk = AHKActions()


def open_menu():
    ahk.move(1770, 80)
    ahk.click()

def open_souls_menu():
    ahk.move(1340, 340)
    ahk.click()

def open_collections_menu():
    ahk.move(650, 200)
    ahk.click()

def open_not_collected():
    ahk.move(400, 1000)
    ahk.click()

def extend_collection():
    ahk.move(850, 300)
    ahk.click()

def reset_collection_menu():
    ahk.move(400, 185)
    ahk.click()

    open_collections_menu()

def fuse_souls_collection():
    ahk.move(1000, 660)
    ahk.click()

    time.sleep(1.5)

    ahk.move(1000, 940)
    ahk.click()

    time.sleep(3)

    ahk.move(700, 940)
    ahk.click()

def fuse_souls():
    ahk.move(950, 950)
    ahk.click()

    ahk.move(950, 670)
    ahk.click()
