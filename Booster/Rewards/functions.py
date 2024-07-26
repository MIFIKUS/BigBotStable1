from Booster.MainClasses.classes import Image


image = Image()


def reward_available() -> bool:
    image.take_screenshot('Booster\\Rewards\\imgs\\screenshots\\is_reward_available.png', (1560, 244, 1825, 325))
    return image.matching('Booster\\Rewards\\imgs\\screenshots\\is_reward_available.png',
                          'Booster\\Rewards\\imgs\\templates\\reward_available.png')


