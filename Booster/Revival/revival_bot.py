from Booster.Revival import ingame_actions
from Booster.Revival.functions import Revive, AccActions
from Booster.MainClasses.classes import AHKActions, Windows

import TGNotifier

import time
import json


MIN_BALANCE = 200
IGNORE_CATEGORIES = (2, 4)
LIST_OF_REVIVES = ('ERATHONA', 'POLINA', 'NEVITH', 'KALLI', 'ANAKHIM')
REVIVE_COLORS = ('yellow', 'green', 'purple', 'blue')

with open('Booster\\Revival\\revivals_lvls_cords.json') as lvls_cords_json:
    LVL_CORDS = json.load(lvls_cords_json)

ahk = AHKActions()
windows = Windows()

revive = Revive()
acc = AccActions()


def main():
    try:
        ingame_actions.open_menu()
        ingame_actions.open_revival_menu()

        time.sleep(3)

        category_counter = 0
        for i in range(7):
            if i in IGNORE_CATEGORIES:
                continue

            ingame_actions.switch_revival_class(i)
            time.sleep(3)

            if acc.get_balance() < 200:
                print('Недостаточный баланс')
                ahk.esc()
                return

            category_cords = LVL_CORDS.get(LIST_OF_REVIVES[category_counter])

            category_yellow_cords = category_cords.get('yellow')
            category_green_cords = category_cords.get('green')
            category_purple_cords = category_cords.get('purple')
            category_blue_cords = category_cords.get('blue')

            category_counter += 1

            for j in REVIVE_COLORS:
                if j == 'yellow':
                    cords = category_yellow_cords
                elif j == 'green':
                    cords = category_green_cords
                elif j == 'purple':
                    cords = category_purple_cords
                elif j == 'blue':
                    cords = category_blue_cords

                if cords is None:
                    continue

                for lvl, cords in cords.items():
                    balance = acc.get_balance()
                    print(f'Баланс: {balance}')
                    if balance < 200:
                        ahk.esc()
                        return

                    ingame_actions.click_on_revive_lvl(cords[0], cords[1])
                    time.sleep(1)

                    if revive.revive_availible():
                        revive.revive()

            for _ in range(2):
                ahk.esc()
    except Exception as e:
        TGNotifier.send_break_msg('Пробуждение', '', e)

def run():
    windows.switch_windows(main)
