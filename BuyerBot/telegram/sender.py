import telebot
import urllib3


LIST_OF_USERS = [760238501]
#, 420909529, 1971488921
TG_API_KEY = '7118021557:AAEE6oPHidJ4utXxSOdT6kuBOe2NF62SOVk'
UNKNOWN_ITEMS_API_KEY = '6866596307:AAGQP7Y6RpFfh54C8YYx8Tg3eetMvW7smbE'

bot = telebot.TeleBot(TG_API_KEY)
unknown_items_bot = telebot.TeleBot(UNKNOWN_ITEMS_API_KEY)


def low_price_notification(item_name, price, server, item_color):
    if item_color == 'purple':
        color = 'Фиол'
    elif item_color == 'red':
        color = 'Красная'
    elif item_color == 'blue':
        color = 'Синька'
    else:
        color = ''

    text = f"*{item_name}({price}💎)* {color}\n"\
           f"Сервер {server}"

    for i in LIST_OF_USERS:
        bot.send_message(i, text,  parse_mode="Markdown")

def unknown_item_notification(item_id, item_name, img_link, color):
    COLORS = {'red': 'Красная', 'purple': 'Фиол', 'special': 'Особое', 'grey': 'Серая'}

    color = COLORS.get(color)

    text = f'{img_link}\n{item_id} {item_name} {color}'

    for i in LIST_OF_USERS:
        unknown_items_bot.send_message(i, text)
