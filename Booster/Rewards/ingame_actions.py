from Booster.MainClasses.classes import AHKActions

ahk = AHKActions()


def open_journal():
    ahk.move(1690, 80)
    ahk.click()


def open_rewards():
    ahk.move(1000, 200)
    ahk.click()


def collect_reward():
    ahk.move(1600, 300)
    ahk.click()


def apply_reward():
    ahk.move(900, 770)
    ahk.click()


def close_journal():
    ahk.move(1800, 90)
    ahk.click()
