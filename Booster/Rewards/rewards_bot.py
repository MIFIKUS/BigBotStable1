from Booster.Rewards.functions import *
from Booster.Rewards.ingame_actions import *

from Booster.MainClasses.classes import Windows

import time


windows = Windows()


def main():
    open_journal()
    time.sleep(3)

    open_rewards()
    time.sleep(2)

    collected_rewards_amount = 0

    while reward_available():
        collected_rewards_amount += 1
        collect_reward()
        apply_reward()
        time.sleep(1)

        if collected_rewards_amount == 100:
            break

    close_journal()


def run():
    windows.switch_windows(main)



