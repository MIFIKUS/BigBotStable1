from Booster.MainClasses.classes import AHKActions, Windows
from Booster.Stamps import ingame_actions
from Booster.Stamps.functions import ImpressStamps
import time


ahk = AHKActions()
windows = Windows()

impress = ImpressStamps()


def main():
    ingame_actions.open_menu()
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
    windows.switch_windows(main)