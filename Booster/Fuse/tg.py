import telebot
import json

with open('Booster\\Fuse\\services_files\\tg.json', encoding='utf-8') as tg_file:
    tg_dict = json.load(tg_file)


class TGBot:
    def __init__(self):
        self._api_key = tg_dict.get('API_KEY')
        self._tg_id = tg_dict.get('TG_ID')
        self._bot = telebot.TeleBot(self._api_key)


    def send_red_aghathion_message(self, aghathion_name, acc_name):
        msg_text = f"""
        Выпал агатион: {aghathion_name}\n
        Аккаунт: {acc_name}
        """

        self._bot.send_message(self._tg_id, msg_text)

    def send_red_class_message(self, class_name, acc_name):
        msg_text = f"""
        Выпал класс: {class_name}\n
        Аккаунт: {acc_name}
        """

        self._bot.send_message(self._tg_id, msg_text)




