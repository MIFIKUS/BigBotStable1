from BuyerBot.jwt_updater.l2m_actions import update_token
from BuyerBot.jwt_updater.fiddler_actions import get_new_token

from BuyerBot.database.get_bot_data import need_to_update_jwt
from BuyerBot.database.update_bot_data import set_jwt_token, set_need_to_update_jwt

import time


DELAY = 10

while True:
    if need_to_update_jwt():
        update_token.update_token()
        token = get_new_token.get_token()

        set_jwt_token(token)
        set_need_to_update_jwt(False)

    time.sleep(DELAY)
