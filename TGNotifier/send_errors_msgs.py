from TGNotifier import API_KEY, LIST_OF_RECEIVERS
import telebot


bot = telebot.TeleBot(API_KEY)


def send_break_msg(bot_name: str, acc_name: str, error: str):
    text = f"Аккаунт: {acc_name}\n{bot_name} сломался. Ошибка {error}"
    for i in LIST_OF_RECEIVERS:
        bot.send_message(i, text)


def send_overflow_msg(acc_name: str):
    text = f"Аккаунт: {acc_name} переполнен"
    for i in LIST_OF_RECEIVERS:
        bot.send_message(i, text)


def send_probably_break(bot_name: str, acc_name: str, error: str):
    text = f"Аккаунт: {acc_name}\n{bot_name} скорее всего сломался. Ошибка {error}"
    for i in LIST_OF_RECEIVERS:
        bot.send_message(i, text)




