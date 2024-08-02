from Booster.MainClasses.classes import AHKActions, Windows
from Booster.Stamps import ingame_actions
from Booster.Stamps.functions import ImpressStamps

import TGNotifier
import time


ahk = AHKActions()
windows = Windows()

impress = ImpressStamps()


def main():
    while not impress.menu_opened():
        ingame_actions.open_menu()
        time.sleep(1)

    ingame_actions.open_stamps_menu()

    for i in range(8):
        ingame_actions.go_next_stamp(i)
        time.sleep(3)

        if impress.impress() is False:
            ahk.esc()
            time.sleep(1)
            break
    ahk.esc()

def run():
    try:
        windows.switch_windows(main)
    except Exception as e:
        TGNotifier.send_break_msg('Печати', '', e)