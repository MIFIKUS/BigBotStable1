from Booster.Souls import ingame_actions
from Booster.Souls import functions
from Booster.MainClasses.classes import AHKActions, Windows

import TGNotifier
import time

ahk = AHKActions()
windows = Windows()

def main():
    ingame_actions.open_menu()
    ingame_actions.open_souls_menu()

    if functions.is_fuse_availible():
        ingame_actions.fuse_souls()
        time.sleep(2)
        functions.skip_fuse()

    ingame_actions.open_collections_menu()
    time.sleep(2)

    ingame_actions.open_not_collected()

    no_more_collections = False
    while no_more_collections is False:
        ingame_actions.extend_collection()
        time.sleep(1)

        collection_percents = functions.get_fuse_percents()

        if collection_percents != 100:
            no_more_collections = True
        else:
            ingame_actions.fuse_souls_collection()
            time.sleep(5)
    ahk.esc()

def run():
    try:
        windows.switch_windows(main)
    except Exception as e:
        TGNotifier.send_break_msg('Души', '', e)
