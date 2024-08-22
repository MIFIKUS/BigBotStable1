from Booster.Fuse.fuse_bot import main as fuse
from Booster.Souls.souls_bot import main as souls
from Booster.Revival.revival_bot import main as revival
from Booster.Cases.cases_bot import main as cases
from Booster.Stamps.stamps_bot import main as stamps
from Booster.Rewards.rewards_bot import main as rewards
from Booster.Scrolls.scrolls_bot import main as scrolls

from BotForCards.botForCards import run as cards

from Booster.MainClasses.classes import Windows


import time


windows = Windows()
try:
    with open('settings.txt', 'r', encoding='utf-8') as settings_txt:
        settings = settings_txt.read()
        settings.split('\n')
        for i in settings:
            if 'path' in i:
                path = i.split('=')[1]
except:
    with open('settings.txt', 'r', encoding='windows-1251') as settings_txt:
        settings = settings_txt.read()
        settings.split('\n')
        for i in settings:
            if 'path' in i:
                path = i.split('=')[1]



def start_all_bots():
    print('Начало работы карточек')
    cards(1, path)
    print('Конец работы карточек')

    print('Начало работы фьюза')
    fuse()
    time.sleep(2)
    print('Конец работы фьюза')

    print('Начало работы душ')
    souls()
    time.sleep(2)
    print('Конец работы душ')

    print('Начало работы пробуды')
    revival()
    time.sleep(2)
    print('Конец работы пробуды')

    print('Начало работы сундуков')
    cases()
    time.sleep(2)
    print('Конец работы сунудков')

    print('Начало работы печатей')
    stamps()
    time.sleep(2)
    print('Конец работы печатей')

    print('Начало работы наград')
    rewards()
    time.sleep(2)
    print('Конец работы наград')

    print('Начало работы знаков')
    scrolls()
    time.sleep(2)
    print('Конец работы знаков')


def run():
    windows.switch_windows(start_all_bots)