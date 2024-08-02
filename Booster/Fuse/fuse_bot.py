from Booster.MainClasses.classes import AHKActions, Image, Windows
from Booster.Fuse import ingame_actions
from Booster.Fuse.functions import FuseClasses, ConfirmMenu, Checks

import TGNotifier
import time

ahk = AHKActions()
image = Image()
windows = Windows()
fuse = FuseClasses()
confirm_menu = ConfirmMenu()


def fuse_classes():
    print('Начинается процесс слияния классов')

    while not Checks.menu_opened():
        ingame_actions.open_menu()
        time.sleep(1)

    print('Меню открылось')

    ingame_actions.open_classes_menu()
    time.sleep(5)

    print('Меню классов открылось')

    ingame_actions.open_fusion_menu()
    time.sleep(3)

    print('Меню слияния открылось')

    while True:
        if fuse.make_fuse() is False:
            print('Больше нет карточек для слияния')
            break
        print('Есть карточки для слияния')

        ingame_actions.reset_fuse_menu()

    print('Открытие меню подтверждения')

    if confirm_menu.need_to_confirm(False):
        ingame_actions.open_confirm_red_menu()
        print('Доступны карточки для подтверждения')

    while confirm_menu.need_to_confirm(False):
        confirm_menu.confirm(False)
        time.sleep(3)

        print('Карточка подтверждена')

    ahk.esc()


def fuse_aghathions():
    while not Checks.menu_opened():
        ingame_actions.open_menu()
        time.sleep(1)

    ingame_actions.open_aghathions_menu()
    time.sleep(5)

    ingame_actions.open_fusion_menu_aghathion()
    time.sleep(3)

    while True:
        if fuse.make_fuse() is False:
            break

        ingame_actions.reset_fuse_menu_aghathion()

    if confirm_menu.need_to_confirm(True):
        ingame_actions.open_confirm_red_menu_aghathion()

    while confirm_menu.need_to_confirm(True):
        confirm_menu.confirm(True)
        time.sleep(3)

    ahk.esc()

def main():
    fuse_classes()
    fuse_aghathions()


def run():
    windows.switch_windows(main)
