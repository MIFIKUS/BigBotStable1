from Autosell import AutoSellBotFinal
from Autosell import market_header_updater
from CheckGreen import BotForCheckingGreen
from SborPlushek import script_dlya_sbora_plushek
from BotForCards import botForCards
from BotForStats import BotForStat
from Alchemy import AlchemyBot
from CollectionMaster import collection_master
from Booster.Fuse import fuse_bot
from Booster.Souls import souls_bot
from Booster.Stamps import stamps_bot
from Booster.Revival import revival_bot
from Booster.Cases import cases_bot
from Booster.Rewards import rewards_bot
from Booster.Scrolls import scrolls_bot
from Booster.All import start_all_boosters


import tkinter as tk
from tkinter import ttk
import json
import multiprocessing
import asyncio

import update_statistics

LIST_OF_ROLLS = (
    'Roll_00',
    'Roll_000',
    'Roll_66',
    'Roll_66_Lite',
    'Roll_32',
    'Roll_80',
    'Roll_80_Red',
    'Roll_888',
    'Roll_888_K',
    'Roll_40',
    'Roll_40_Symbol',
    'Roll_50',
    'Roll_50_Symbol',
    'Roll_50_Symbol_Plus')

def con(obj,color):
    print(color)
    obj.configure(bg=color)

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry('1290x1080')
        self['bg'] = '#282828'
        self.frames = {}
        for F in (Main, AllBots, BuyerSettings, SborPlushekSettings, AutoSellSettings, BotForStatSettings, GreenCheckSettings, MainSettings,
                  AllBotsSecondPage, AlchemySettings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Main")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

def start_main_bots():
    pass


def Buyer():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'BuyerBot_choosed_mode' in i:
                mode = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'BuyerBot_minimal_price' in i:
                minimal_price = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'BuyerBot_minimal_price_for_red' in i:
                minimal_price_for_red = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'BuyerBot_minimal_price_for_red_acessories' in i:
                minimal_price_for_red_accesories = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'BuyerBot_amount_items_to_buy' in i:
                amount_items_to_buy = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'BuyerBot_schedule' in i:
                schedule = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'multiplier' in i:
                multiplier = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                print(i)
                break



def Autosell():
    if __name__ == '__main__':
        with open('settings.txt') as f:
            for i in f.readlines():
                if 'AutoSell_schedule' in i:
                    schedule = i.split('=')[1]
                    print(i)
                    break

        with open('settings.txt') as f:
            for i in f.readlines():
                if 'multiplier' in i:
                    multiplier = i.split('=')[1]
                    print(i)
                    break

        with open('settings.txt') as f:
            for i in f.readlines():
                if 'path' in i:
                    path = i.split('=')[1]
                    print(i)
                    break

        autosell = multiprocessing.Process(target=AutoSellBotFinal.run, args=(schedule, multiplier, path,))
        autosell.start()

        headers_updater = multiprocessing.Process(target=market_header_updater.run)
        headers_updater.start()


def CheckGreen():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'GreenCheck_hotkey' in i:
                hotkey = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'GreenCheck_mode' in i:
                mode = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'multiplier' in i:
                multiplier = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                print(i)
                break


    if __name__ == '__main__':
        green_check = multiprocessing.Process(target=BotForCheckingGreen.run, args=(hotkey, mode, multiplier,))
        green_check.start()


def SborPlushek():
    def __reset_current_dungeon():
        with open('settings.txt') as f:
            for i in f.readlines():
                if 'SborPlushek_current_dungeon' in i:
                    current_dungeon = i.split('=')
                    break
        with open('settings.txt', 'r') as f:
            old_data = f.read()
            print(current_dungeon[1])
            new_data = old_data.replace(f'SborPlushek_current_dungeon={current_dungeon[1]}',
                                        f'SborPlushek_current_dungeon=1\n')
        with open('settings.txt', 'w') as f:
            f.write(new_data)


    __reset_current_dungeon()
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'SborPlushek_schedule' in i:
                schedule = i.split('=')[1]
                print(i)
                break
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'SborPlushek_amount_of_clicks_in_clan' in i:
                clan_clicks = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'multiplier' in i:
                multiplier = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                print(i)
                break

    if __name__ == '__main__':
        sbor_plushek = multiprocessing.Process(target=script_dlya_sbora_plushek.run, args=(clan_clicks, multiplier, path, schedule, 1))
        sbor_plushek.start()

def sbor_plushek_next_dungeon():
    with open('settings.txt') as f:
        current_dungeon = None
        schedule = None
        clan_clicks = None
        multiplier = None
        path = None
        for i in f.readlines():
            if 'SborPlushek_current_dungeon' in i:
                current_dungeon = i.split('=')[1]
                print('current_dungeon_num is', current_dungeon)
            if 'SborPlushek_schedule' in i:
                schedule = i.split('=')[1]
                print(i)
            if 'SborPlushek_amount_of_clicks_in_clan' in i:
                clan_clicks = i.split('=')[1]
                print(i)
            if 'multiplier' in i:
                multiplier = i.split('=')[1]
                print(i)
            if 'path' in i:
                path = i.split('=')[1]
                print(i)

    if __name__ == '__main__':
        sbor_plushek = multiprocessing.Process(target=script_dlya_sbora_plushek.run,
                                               args=(clan_clicks, multiplier, path, schedule, current_dungeon))
        sbor_plushek.start()

def sbor_plushek_apples():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                print(i)
    if __name__ == '__main__':
        apples = multiprocessing.Process(target=script_dlya_sbora_plushek.start_collect_apples,
                                                   args=(path,))
        apples.start()

def sbor_plushek_collect_event_good():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                print(i)

    if __name__ == '__main__':
        event = multiprocessing.Process(target=script_dlya_sbora_plushek.start_collect_event_good,
                                                   args=(path,))
        event.start()


def BotForCards():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'multiplier' in i:
                multiplier = i.split('=')[1]
                print(i)
                break

    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                print(i)
                break
    if __name__ == '__main__':
        bot_cards = multiprocessing.Process(target=botForCards.run, args=(multiplier, path,))
        bot_cards.start()

def BotForStats():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'BotForStat_statlist' in i:
                statlist = i.split('=')[1]
                print(i)
                break
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'multiplier' in i:
                multiplier = i.split('=')[1]
                print(i)
                break


    if __name__ == '__main__':
        bot_for_stat = multiprocessing.Process(target=BotForStat.run, args=(statlist, multiplier,))
        bot_for_stat.start()

def alchemy_bot():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                print(i)
            if 'Alchemy_minimal_price' in i:
                minimal_price = i.split('=')[1]
                print(i)
    if __name__ == '__main__':
        alchemy = multiprocessing.Process(target=AlchemyBot.main, args=(path,))
        alchemy.start()

def collections():
    if __name__ == '__main__':
        collection = multiprocessing.Process(target=collection_master.run)
        collection.start()

class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def default_statistics():
            accs_labels = []
            balance_labels = []
            sold_items_labels = []
            all_income_labels = []
            balance_on_market_labels = []
            amount_on_market_labels = []
            accs = []
            balance = []
            sold_items = []
            all_income = []
            balance_on_market = []
            amount_on_market = []

            with open('statistics.json', encoding='utf-8') as statistics_json:
                statistics = json.load(statistics_json)
                print(statistics.items())
                for i in statistics.items():
                    print(i)
                    accs_labels.append(tk.Label(self, text='Аккаунт', bg='#282828',fg='#d4d3d3',font='Arial 20'))
                    balance_labels.append(tk.Label(self, text='Баланс', bg='#282828',fg='#d4d3d3',font='Arial 20'))
                    sold_items_labels.append(tk.Label(self, text='Продано', bg='#282828',fg='#d4d3d3',font='Arial 20'))
                    all_income_labels.append(tk.Label(self, text='Доход', bg='#282828',fg='#d4d3d3',font='Arial 20'))
                    balance_on_market_labels.append(tk.Label(self, text='Баланс на ауке', bg='#282828',fg='#d4d3d3',font='Arial 20'))
                    amount_on_market_labels.append(tk.Label(self, text='Слоты на ауке', bg='#282828',fg='#d4d3d3',font='Arial 20'))

                    accs.append(tk.Label(self, text=i[0], bg='#282828',fg='#24c9c3',font='Arial 20',borderwidth=0))
                    balance.append(tk.Label(self, text=i[1]['Баланс на акке'], bg='#282828',fg='#24c9c3',font='Arial 20',borderwidth=0))
                    sold_items.append(tk.Label(self, text=i[1]['Продано шмоток'], bg='#282828',fg='#24c9c3',font='Arial 20',borderwidth=0))
                    all_income.append(tk.Label(self, text=i[1]['Общий доход с продаж'], bg='#282828',fg='#24c9c3',font='Arial 20',borderwidth=0))
                    balance_on_market.append(tk.Label(self, text=i[1]['Баланс на ауке'], bg='#282828',fg='#24c9c3',font='Arial 20',borderwidth=0))
                    amount_on_market.append(tk.Label(self, text=i[1]['кол-во шмоток в ауке'], bg='#282828',fg='#24c9c3',font='Arial 20',borderwidth=0))

            y=100
            x=100
            for i in accs_labels:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=100


            y=150
            x=100
            for i in balance_labels:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=150

            y=190
            x=100
            for i in sold_items_labels:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=190

            y=230
            x=100
            for i in all_income_labels:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=230

            y=270
            x=100
            for i in balance_on_market_labels:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=270

            y=310
            x=100
            for i in amount_on_market_labels:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=310


            y=100
            x=310
            for i in accs:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=100

            y=150
            x=310
            for i in balance:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=150

            y=190
            x=310
            for i in sold_items:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=190

            y=230
            x=310
            for i in all_income:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=230

            y=270
            x=310
            for i in balance_on_market:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=270

            y=310
            x=310
            for i in amount_on_market:
                i.place(x=x, y=y)
                y+=210
                if y > 900:
                    x+=300
                    y=310

            print(accs)
            print(balance)
            print(sold_items)
            print(all_income)


        def update_statistiks():
            update_statistics.run()




        self['bg'] = '#282828'
        go_to_all_bots = tk.Button(self, text="Все боты" ,background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth=0, compound='center',font='Arial 24', command=lambda: controller.show_frame('AllBots'))
        go_to_main = tk.Button(self, text="Главная", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center', font='Arial 24')
        go_to_settings = tk.Button(self, text="Настройки", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center',font='Arial 24', command=lambda: controller.show_frame('MainSettings'))
        update_statistic = tk.Button(self, text="Обновить", background='#535353', fg='#d4d3d3', height=2, width=12, borderwidth = 0, compound='center',font='Arial 24', command=update_statistiks)


        go_to_all_bots.bind('<Enter>', lambda event, h=go_to_all_bots: con(h, '#404040'))
        go_to_all_bots.bind("<Leave>", lambda event, h=go_to_all_bots: con(h, "#535353"))
        go_to_main.bind('<Enter>', lambda event, h=go_to_main:con(h, '#404040'))
        go_to_main.bind("<Leave>", lambda event, h=go_to_main: con(h, "#535353"))
        go_to_settings.bind('<Enter>', lambda event, h=go_to_settings: con(h, '#404040'))
        go_to_settings.bind("<Leave>", lambda event, h=go_to_settings: con(h, "#535353"))


        go_to_all_bots.place(x=0, y=0)
        go_to_main.place(x=430, y=0)
        go_to_settings.place(x=860, y=0)

        update_statistic.place(x=860, y=920)
        default_statistics()



class AllBots(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'
        go_to_all_bots = tk.Button(self, text="Все боты" ,background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth=0, compound='center',font='Arial 24', command=lambda: controller.show_frame('AllBots'))
        go_to_main = tk.Button(self, text="Главная", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center', font='Arial 24', command=lambda: controller.show_frame('Main'))
        go_to_settings = tk.Button(self, text="Настройки", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center',font='Arial 24', command=lambda: controller.show_frame('MainSettings'))

        go_to_all_bots.bind('<Enter>', lambda event, h=go_to_all_bots: con(h, '#404040'))
        go_to_all_bots.bind("<Leave>", lambda event, h=go_to_all_bots: con(h, "#535353"))
        go_to_main.bind('<Enter>', lambda event, h=go_to_main:con(h, '#404040'))
        go_to_main.bind("<Leave>", lambda event, h=go_to_main: con(h, "#535353"))
        go_to_settings.bind('<Enter>', lambda event, h=go_to_settings: con(h, '#404040'))
        go_to_settings.bind("<Leave>", lambda event, h=go_to_settings: con(h, "#535353"))

        buyer_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        buyer_label = tk.Label(self, text='Скупщик', bg='#404040',fg='#d4d3d3',font='Arial 24')

        buyer_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41',font='Arial 24',borderwidth=0,command=Buyer)
        buyer_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3',font='Arial 24',borderwidth=0)
        buyer_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e',font='Arial 24',borderwidth=0, command=lambda: controller.show_frame('BuyerSettings'))

        buyer_start_button.bind('<Enter>', lambda event, h=buyer_start_button: h.configure(fg='#459330'))
        buyer_start_button.bind("<Leave>", lambda event, h=buyer_start_button: h.configure(fg='#5ecb41'))

        buyer_logs_button.bind('<Enter>', lambda event, h=buyer_logs_button: h.configure(fg='#1b9591'))
        buyer_logs_button.bind("<Leave>", lambda event, h=buyer_logs_button: h.configure(fg='#24c9c3'))

        buyer_settings_button.bind('<Enter>', lambda event, h=buyer_settings_button: h.configure(fg='#875520'))
        buyer_settings_button.bind("<Leave>", lambda event, h=buyer_settings_button: h.configure(fg='#c17a2e'))

        bot_for_raking_rewards_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        bot_for_raking_rewards_label = tk.Label(self, text='Бот для сбора плюшек', bg='#404040',fg='#d4d3d3',font='Arial 24')

        bot_for_raking_rewards_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41',font='Arial 24',borderwidth=0, command=lambda: SborPlushek())

        bot_for_raking_rewards_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e',font='Arial 24',borderwidth=0, command=lambda: controller.show_frame('SborPlushekSettings'))
        bot_for_taking_rewards_next_button = tk.Button(self, text='Некст данж', bg='#404040', fg='#24c9c3',font='Arial 24',borderwidth=0, command=lambda: sbor_plushek_next_dungeon())
        bot_for_taking_rewards_apples_button = tk.Button(self, text='Яблоки', bg='#404040', fg='#F24F44', font='Arial 24', borderwidth=0, command=lambda: sbor_plushek_apples())
        bot_for_taking_rewards_event_button = tk.Button(self, text='Ивент', bg='#404040', fg='#F24F44', font='Arial 24', borderwidth=0, command=lambda: sbor_plushek_collect_event_good())

        bot_for_raking_rewards_start_button.bind('<Enter>', lambda event, h=bot_for_raking_rewards_start_button: h.configure(fg='#459330'))
        bot_for_raking_rewards_start_button.bind("<Leave>", lambda event, h=bot_for_raking_rewards_start_button: h.configure(fg='#5ecb41'))

        alchemy_frame = tk.Frame(self, bg='#404040', width=1260, height=150)
        alchemy_label = tk.Label(self, text='Алхимка', bg='#404040', fg='#d4d3d3', font='Arial 24')

        alchemy_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41', font='Arial 24', borderwidth=0,
                                         command=lambda: alchemy_bot())
        alchemy_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3', font='Arial 24', borderwidth=0)
        alchemy_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e', font='Arial 24',
                                            borderwidth=0, command=lambda: controller.show_frame('AlchemySettings'))

        #bot_for_raking_rewards_logs_button.bind('<Enter>', lambda event, h=bot_for_raking_rewards_logs_button: h.configure(fg='#1b9591'))
        #bot_for_raking_rewards_logs_button.bind("<Leave>", lambda event, h=bot_for_raking_rewards_logs_button: h.configure(fg='#24c9c3'))

        bot_for_raking_rewards_settings_button.bind('<Enter>', lambda event, h=bot_for_raking_rewards_settings_button: h.configure(fg='#875520'))
        bot_for_raking_rewards_settings_button.bind("<Leave>", lambda event, h=bot_for_raking_rewards_settings_button: h.configure(fg='#c17a2e'))

        buyer_frame.place(x=15, y=120)
        buyer_label.place(x=60, y=140)

        buyer_start_button.place(x=50, y=190)
        buyer_logs_button.place(x=210, y=190)
        buyer_settings_button.place(x=350,y=190)


        bot_for_raking_rewards_frame.place(x=15, y=290)
        bot_for_raking_rewards_label.place(x=60, y=310)

        bot_for_raking_rewards_start_button.place(x=50, y=360)
        bot_for_raking_rewards_settings_button.place(x=170, y=360)
        bot_for_taking_rewards_next_button.place(x=350, y=360)
        bot_for_taking_rewards_apples_button.place(x=550, y=360)
        bot_for_taking_rewards_event_button.place(x=700, y=360)

        #cards_frame.place(x=15, y=630)
        #cards_label.place(x=60, y=650)
        #cards_start_button.place(x=50, y=700)
        #cards_logs_button.place(x=210, y=700)

        alchemy_frame.place(x=15, y=630)
        alchemy_label.place(x=60, y=650)

        alchemy_start_button.place(x=50, y=700)
        alchemy_logs_button.place(x=210, y=700)
        alchemy_settings_button.place(x=350,y=700)

        go_to_all_bots.place(x=0, y=0)
        go_to_main.place(x=430, y=0)
        go_to_settings.place(x=860, y=0)


        autosell_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        autosell_label = tk.Label(self, text='Автоперестановка', bg='#404040',fg='#d4d3d3',font='Arial 24')

        autosell_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41',font='Arial 24',borderwidth=0, command=lambda: Autosell())
        autosell_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3',font='Arial 24',borderwidth=0)
        autosell_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e',font='Arial 24', borderwidth=0, command=lambda: controller.show_frame('AutoSellSettings'))

        autosell_start_button.bind('<Enter>', lambda event, h=autosell_start_button: h.configure(fg='#459330'))
        autosell_start_button.bind("<Leave>", lambda event, h=autosell_start_button: h.configure(fg='#5ecb41'))

        autosell_logs_button.bind('<Enter>', lambda event, h=autosell_logs_button: h.configure(fg='#1b9591'))
        autosell_logs_button.bind("<Leave>", lambda event, h=autosell_logs_button: h.configure(fg='#24c9c3'))

        autosell_settings_button.bind('<Enter>', lambda event, h=autosell_settings_button: h.configure(fg='#875520'))
        autosell_settings_button.bind("<Leave>", lambda event, h=autosell_settings_button: h.configure(fg='#c17a2e'))

        #cards_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        #cards_label = tk.Label(self, text='Бот для сбора карточек', bg='#404040', fg='#d4d3d3', font='Arial 24')

        #cards_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41',font='Arial 24', borderwidth=0, command=lambda: BotForCards())
        #cards_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3',font='Arial 24', borderwidth=0)

        go_to_next_page = tk.Button(self, text="🢂", background='#d4d3d3', fg='#535353', height=1, width=2, borderwidth = 0, compound='center',font='Arial 24', command=lambda: controller.show_frame('AllBotsSecondPage'))


        #cards_start_button.bind('<Enter>', lambda event, h=cards_start_button: h.configure(fg='#459330'))
        #cards_start_button.bind("<Leave>", lambda event, h=cards_start_button: h.configure(fg='#5ecb41'))

        #cards_logs_button.bind('<Enter>', lambda event, h=cards_logs_button: h.configure(fg='#1b9591'))
        #cards_logs_button.bind("<Leave>", lambda event, h=cards_logs_button: h.configure(fg='#24c9c3'))

        check_green_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        check_green_label = tk.Label(self, text='Бот для проверки зеленого', bg='#404040', fg='#d4d3d3', font='Arial 24')

        check_green_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41',font='Arial 24', borderwidth=0, command=lambda: CheckGreen())
        check_green_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3',font='Arial 24', borderwidth=0)
        check_green_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e',font='Arial 24', borderwidth=0, command=lambda: controller.show_frame('GreenCheckSettings'))

        check_green_start_button.bind('<Enter>', lambda event, h=check_green_start_button: h.configure(fg='#459330'))
        check_green_start_button.bind("<Leave>", lambda event, h=check_green_start_button: h.configure(fg='#5ecb41'))

        check_green_logs_button.bind('<Enter>', lambda event, h=check_green_logs_button: h.configure(fg='#1b9591'))
        check_green_logs_button.bind("<Leave>", lambda event, h=check_green_logs_button: h.configure(fg='#24c9c3'))

        check_green_settings_button.bind('<Enter>', lambda event, h=check_green_settings_button: h.configure(fg='#875520'))
        check_green_settings_button.bind("<Leave>", lambda event, h=check_green_settings_button: h.configure(fg='#c17a2e'))

        buyer_frame.place(x=15, y=120)
        buyer_label.place(x=60, y=140)

        buyer_start_button.place(x=50, y=190)
        buyer_logs_button.place(x=210, y=190)
        buyer_settings_button.place(x=350,y=190)


        bot_for_raking_rewards_frame.place(x=15, y=290)
        bot_for_raking_rewards_label.place(x=60, y=310)
        #bot_for_raking_rewards_start_button.place(x=50, y=360)
        #bot_for_raking_rewards_settings_button.place(x=350,y=360)

        autosell_frame.place(x=15, y=460)
        autosell_label.place(x=60, y=480)

        autosell_start_button.place(x=50, y=530)
        autosell_logs_button.place(x=210, y=530)
        autosell_settings_button.place(x=350, y=530)


        #cards_frame.place(x=15, y=630)
        #cards_label.place(x=60, y=650)
        #cards_start_button.place(x=50, y=700)
        #cards_logs_button.place(x=210, y=700)


        check_green_frame.place(x=15, y=800)
        check_green_label.place(x=60, y=820)
        check_green_start_button.place(x=50, y=870)
        check_green_logs_button.place(x=210, y=870)
        check_green_settings_button.place(x=350, y=870)

        go_to_all_bots.place(x=0, y=0)
        go_to_main.place(x=430, y=0)
        go_to_settings.place(x=860, y=0)

        go_to_next_page.place(x=1200, y=500)

class AllBotsSecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'

        go_to_all_bots = tk.Button(self, text="Все боты" ,background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth=0, compound='center',font='Arial 24', command=lambda: controller.show_frame('AllBots'))
        go_to_main = tk.Button(self, text="Главная", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center', font='Arial 24', command=lambda: controller.show_frame('Main'))
        go_to_settings = tk.Button(self, text="Настройки", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center',font='Arial 24', command=lambda: controller.show_frame('MainSettings'))

        go_to_all_bots.bind('<Enter>', lambda event, h=go_to_all_bots: con(h, '#404040'))
        go_to_all_bots.bind("<Leave>", lambda event, h=go_to_all_bots: con(h, "#535353"))
        go_to_main.bind('<Enter>', lambda event, h=go_to_main:con(h, '#404040'))
        go_to_main.bind("<Leave>", lambda event, h=go_to_main: con(h, "#535353"))
        go_to_settings.bind('<Enter>', lambda event, h=go_to_settings: con(h, '#404040'))
        go_to_settings.bind("<Leave>", lambda event, h=go_to_settings: con(h, "#535353"))

        bot_for_stat_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        bot_for_stat_label = tk.Label(self, text='Бот для стат', bg='#404040',fg='#d4d3d3',font='Arial 24')

        bot_for_stat_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41',font='Arial 24',borderwidth=0, command=lambda: BotForStats())
        bot_for_stat_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3',font='Arial 24',borderwidth=0)
        bot_for_stat_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e',font='Arial 24', borderwidth=0, command=lambda: controller.show_frame('BotForStatSettings'))

        #alchemy_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        #alchemy_label = tk.Label(self, text='Алхимка', bg='#404040',fg='#d4d3d3',font='Arial 24')

        #alchemy_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41',font='Arial 24',borderwidth=0, command=lambda: alchemy_bot())
        #alchemy_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3',font='Arial 24',borderwidth=0)
        #alchemy_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e',font='Arial 24', borderwidth=0, command=lambda: controller.show_frame('AlchemySettings'))

        go_to_previous_page = tk.Button(self, text="🢀", background='#d4d3d3', fg='#535353', height=1, width=2, borderwidth = 0, compound='center',font='Arial 24', command=lambda: controller.show_frame('AllBots'))


        bot_for_stat_start_button.bind('<Enter>', lambda event, h=bot_for_stat_start_button: h.configure(fg='#459330'))
        bot_for_stat_start_button.bind("<Leave>", lambda event, h=bot_for_stat_start_button: h.configure(fg='#5ecb41'))

        bot_for_stat_logs_button.bind('<Enter>', lambda event, h=bot_for_stat_logs_button: h.configure(fg='#1b9591'))
        bot_for_stat_logs_button.bind("<Leave>", lambda event, h=bot_for_stat_logs_button: h.configure(fg='#24c9c3'))

        bot_for_stat_settings_button.bind('<Enter>', lambda event, h=bot_for_stat_settings_button: h.configure(fg='#875520'))
        bot_for_stat_settings_button.bind("<Leave>", lambda event, h=bot_for_stat_settings_button: h.configure(fg='#c17a2e'))

        bot_for_stat_frame.place(x=15, y=120)
        bot_for_stat_label.place(x=60, y=140)

        bot_for_stat_start_button.place(x=50, y=190)
        bot_for_stat_logs_button.place(x=210, y=190)
        bot_for_stat_settings_button.place(x=350,y=190)

        #alchemy_frame.place(x=15, y=290)
        #alchemy_label.place(x=60, y=310)
#
        #alchemy_start_button.place(x=50, y=360)
        #alchemy_logs_button.place(x=210, y=360)
        #alchemy_settings_button.place(x=350,y=360)

        collection_master_frame = tk.Frame(self, bg='#404040', width = 1260, height=150)
        collection_master_label = tk.Label(self, text='Заточка', bg='#404040',fg='#d4d3d3',font='Arial 24')

        collection_master_start_button = tk.Button(self, text='Старт', bg='#404040', fg='#5ecb41', font='Arial 24', borderwidth=0,
                                         command=lambda: collections())
        collection_master_logs_button = tk.Button(self, text='Логи', bg='#404040', fg='#24c9c3', font='Arial 24', borderwidth=0)
        collection_master_settings_button = tk.Button(self, text='Настройки', bg='#404040', fg='#c17a2e', font='Arial 24',
                                            borderwidth=0, )

        collection_master_frame.place(x=15, y=290)
        collection_master_label.place(x=60, y=310)

        collection_master_start_button.place(x=50, y=360)
        collection_master_logs_button.place(x=210, y=360)
        collection_master_settings_button.place(x=350, y=360)

        booster_frame = tk.Frame(self, bg='#404040', width=1260, height=250)
        booster_label = tk.Label(self, text='Бустера', bg='#404040', fg='#d4d3d3', font='Arial 24')

        fuse = tk.Button(self, text='Фьюз', bg='#404040', fg='#5ecb41', font='Arial 24',
                                                   borderwidth=0,
                                                   command=lambda: fuse_bot.run())

        souls = tk.Button(self, text='Души', bg='#404040', fg='#24c9c3', font='Arial 24',
                                                  borderwidth=0,
                                                  command=lambda: souls_bot.run())

        stamps = tk.Button(self, text='Печати', bg='#404040', fg='#c17a2e',
                                                      font='Arial 24',
                                                      borderwidth=0,
                                                      command=lambda: stamps_bot.run())

        revivals = tk.Button(self, text='Пробуждение', bg='#404040', fg='#ff2b2b',
                           font='Arial 24',
                           borderwidth=0,
                           command=lambda: revival_bot.run())

        cases = tk.Button(self, text='Сундуки', bg='#404040', fg='#ffc0cb',
                           font='Arial 24',
                           borderwidth=0,
                           command=lambda: cases_bot.run())

        cards = tk.Button(self, text='Карточки', bg='#404040', fg='#8A2BE2',
                          font='Arial 24',
                          borderwidth=0,
                          command=lambda: BotForCards())

        rewards = tk.Button(self, text='Награды', bg='#404040', fg='#ffd700',
                          font='Arial 24',
                          borderwidth=0,
                          command=lambda: rewards_bot.run())

        sings = tk.Button(self, text='Знаки', bg='#404040', fg='#D71868',
                          font='Arial 24',
                          borderwidth=0,
                          command=lambda: scrolls_bot.run())

        all_boosters = tk.Button(self, text='Все', bg='#404040', fg='#5ecb41',
                          font='Arial 24',
                          borderwidth=0,
                          command=lambda: start_all_boosters.run())

        #collection_master_frame.place(x=15, y=460)
        #collection_master_label.place(x=60, y=480)

        #collection_master_start_button.place(x=50, y=530)
        #collection_master_logs_button.place(x=210, y=530)
        #collection_master_settings_button.place(x=350, y=530)

        booster_frame.place(x=15, y=460)
        booster_label.place(x=60, y=480)

        fuse.place(x=50, y=530)
        souls.place(x=210, y=530)
        stamps.place(x=350, y=530)
        revivals.place(x=500, y=530)
        cases.place(x=750, y=530)
        cards.place(x=920, y=530)
        rewards.place(x=50, y=620)
        sings.place(x=210, y=620)
        all_boosters.place(x=350, y=620)

        go_to_all_bots.place(x=0, y=0)
        go_to_main.place(x=430, y=0)
        go_to_settings.place(x=860, y=0)

        go_to_previous_page.place(x=50, y=500)

class BuyerSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'
        def set_default_amount_to_buy():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_amount_items_to_buy' in i:
                        price = i.split('=')
                        price[1] = price[1].replace(' ', '')
                        print(price[-1])
                        amount_items_to_buy_text.insert(0, price[1][0:-1])
                        print(i)
                        break

        def set_amount_items_to_buy():
            new_text = amount_items_to_buy_text.get()
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_amount_items_to_buy' in i:
                        price = i.split('=')
                        print(i)
                        break

            with open ('settings.txt', 'r') as f:
                old_data = f.read()
                print(price[1])
                new_data = old_data.replace(i, f'BuyerBot_amount_items_to_buy={new_text}\n')
            with open ('settings.txt', 'w') as f:
                f.write(new_data)
            print(123)

        def set_default_minimal_price_for_red_accesories():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_minimal_price_for_red_acessories' in i:
                        price = i.split('=')
                        price[1] = price[1].replace(' ', '')
                        print(price[-1])
                        minimal_price_for_red_accesories_text.insert(0, price[1][0:-1])
                        print(i)
                        break

        def set_BuyerBot_minimal_price_for_red_accesories():
            new_text = minimal_price_for_red_accesories_text.get()
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_minimal_price_for_red_acessories' in i:
                        price = i.split('=')
                        print(i)
                        break
            with open ('settings.txt', 'r') as f:
                old_data = f.read()
                print(price[1])
                new_data = old_data.replace(f'BuyerBot_minimal_price_for_red_acessories={price[1]}', f'BuyerBot_minimal_price_for_red_acessories={new_text}\n')
            with open ('settings.txt', 'w') as f:
                f.write(new_data)
            print(123)


        def set_default_minimal_price_for_red():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_minimal_price_for_red' in i:
                        price = i.split('=')
                        price[1] = price[1].replace(' ', '')
                        print(price[-1])
                        minimal_price_for_red_text.insert(0, price[1][0:-1])
                        print(i)
                        break

        def set_BuyerBot_minimal_price_for_red():
            new_text = minimal_price_for_red_text.get()
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_minimal_price_for_red' in i:
                        price = i.split('=')
                        print(i)
                        break
            with open ('settings.txt', 'r') as f:
                old_data = f.read()
                print(price[1])
                new_data = old_data.replace(f'BuyerBot_minimal_price_for_red={price[1]}', f'BuyerBot_minimal_price_for_red={new_text}\n')
            with open ('settings.txt', 'w') as f:
                f.write(new_data)
            print(123)

        def set_defaul_schedule_BuyerBot():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_schedule' in i:
                        schedule_list = i.split('=')[1]
                        schedule = schedule_list.split(',')
                        schedule_1_text.insert(-1, schedule[0].replace('(', ''))
                        schedule_2_text.insert(-1, schedule[1])
                        schedule_3_text.insert(-1, schedule[2].replace(')', ''))
                        print(i)
                        break

        def set_BuyerBot_schedule():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_schedule' in i:
                        price = i.split('=')
                        print(i)
                        break
            with open ('settings.txt', 'r') as f:
                old_data = f.read()
                print(price[1])
                schedule_data = []
                schedule_data.append(schedule_1_text.get().replace(' ', '') + ', ')
                schedule_data.append(schedule_2_text.get().replace(' ', '') + ', ')
                schedule_data.append(schedule_3_text.get().replace(' ', '').replace('\n', ''))
                print('Schedule data ',schedule_data)
                new_data = old_data.replace(i, f'BuyerBot_schedule=({"".join(schedule_data)})\n')

            with open ('settings.txt', 'w') as f:
                f.write(new_data)
            print(123)

        def set_default_minimal_price():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_minimal_price' in i:
                        price = i.split('=')
                        price[1] = price[1].replace(' ', '')
                        print(price[-1])
                        minimal_price_text.insert(0, price[1][0:-1])
                        print(i)
                        break

        def set_BuyerBot_minimal_price():
            new_text = minimal_price_text.get()
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BuyerBot_minimal_price' in i:
                        price = i.split('=')
                        print(i)
                        break
            with open ('settings.txt', 'r') as f:
                old_data = f.read()
                print(price[1])
                new_data = old_data.replace(f'BuyerBot_minimal_price={price[1]}', f'BuyerBot_minimal_price={new_text}\n')
            with open ('settings.txt', 'w') as f:
                f.write(new_data)
            print(123)


        def _set_BuyerBot__mode(old_text='', new_text=''):
            for i in range(2):
                with open('settings.txt') as f:
                    for i in f.readlines():
                        if 'BuyerBot_choosed_mode' in i:
                            print(i)
                            chosed_mode_list = i.split('=')
                            chosed_mode = chosed_mode_list[1]
                            break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()

                new_data = old_data.replace(old_text, new_text)

                with open ('settings.txt', 'w') as f:
                    f.write(new_data)

                print(chosed_mode)
                if int(chosed_mode) == 1:
                    mode_1.configure(bg='#5ecb41')
                    mode_2.configure(bg='#535353')
                if int(chosed_mode) == 2:
                    mode_1.configure(bg='#535353')
                    mode_2.configure(bg='#5ecb41')

        mode = tk.Label(self, text='Режим', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)

        mode_1 = tk.Button(self, text="1", bg='#535353', fg='#d4d3d3', width = 5, height=2, font='Arial 24', borderwidth=0, command=lambda: _set_BuyerBot__mode('BuyerBot_choosed_mode=2', 'BuyerBot_choosed_mode=1'))
        mode_2 = tk.Button(self, text="2", bg='#535353', fg='#d4d3d3', width = 5, height=2, font='Arial 24', borderwidth=0, command=lambda: _set_BuyerBot__mode('BuyerBot_choosed_mode=1', 'BuyerBot_choosed_mode=2'))

        _set_BuyerBot__mode()

        minimal_price = tk.Label(self, text='Минимальная цена', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        minimal_price_text = tk.Entry(self, width=16,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 26', justify='center')
        minimal_price_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_BuyerBot_minimal_price)

        minimal_price_for_red = tk.Label(self, text=' Минимальная цена \nдля красных шмоток', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        minimal_price_for_red_text = tk.Entry(self, width=16,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 26', justify='center')
        minimal_price_for_red_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_BuyerBot_minimal_price_for_red)

        minimal_price_for_red_accesories = tk.Label(self, text=' Минимальная цена \nдля аксессуаров', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        minimal_price_for_red_accesories_text = tk.Entry(self, width=16,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 26', justify='center')
        minimal_price_for_red_accesories_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_BuyerBot_minimal_price_for_red_accesories)

        amount_items_to_buy = tk.Label(self, text='Сколько шмоток покупать', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        amount_items_to_buy_text = tk.Entry(self, width=16,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 26', justify='center')
        amount_items_to_buy_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_amount_items_to_buy)


        schedule = tk.Label(self, text='Расписание', bg='#282828', fg='#d4d3d3',font='Arial 24',borderwidth=0)
        schedule_1 = tk.Label(self, text='Время 1', bg='#282828', fg='#d4d3d3',font='Arial 20',borderwidth=0)
        schedule_2 = tk.Label(self, text='Время 2', bg='#282828', fg='#d4d3d3',font='Arial 20',borderwidth=0)
        schedule_3 = tk.Label(self, text='Время 3', bg='#282828', fg='#d4d3d3',font='Arial 20',borderwidth=0)
        schedule_1_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 18', justify='center')
        schedule_2_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 18', justify='center')
        schedule_3_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 18', justify='center')
        schedule_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_BuyerBot_schedule)
        ok_button = tk.Button(self, text='Ок ', height=1, width=8, bg='#535353', fg='#d4d3d3',font='Arial 24',borderwidth=0, command=lambda: controller.show_frame('AllBots'))

        set_default_minimal_price()
        set_defaul_schedule_BuyerBot()
        set_default_minimal_price_for_red()
        set_default_minimal_price_for_red_accesories()
        set_default_amount_to_buy()

        ok_button.bind('<Enter>', lambda event, h=ok_button: con(h, '#404040'))
        ok_button.bind("<Leave>", lambda event, h=ok_button: con(h, "#535353"))

        mode.place(x=200, y=100)
        mode_1.place(x=150, y=170)
        mode_2.place(x=250, y=170)

        minimal_price.place(x=120, y=400)
        minimal_price_text.place(x=110, y=450)
        minimal_price_confirm.place(x=170, y=500)

        minimal_price_for_red.place(x=800, y=100)
        minimal_price_for_red_text.place(x=800, y=200)
        minimal_price_for_red_confirm.place(x=860, y=260)

        minimal_price_for_red_accesories.place(x=800, y=350)
        minimal_price_for_red_accesories_text.place(x=800, y=450)
        minimal_price_for_red_accesories_confirm.place(x=860, y=510)

        amount_items_to_buy.place(x=770,y=600)
        amount_items_to_buy_text.place(x=800, y=650)
        amount_items_to_buy_confirm.place(x=860, y=710)

        schedule.place(x=172, y=700)
        schedule_1.place(x=85, y=750)
        schedule_2.place(x=205, y=750)
        schedule_3.place(x=325, y=750)
        schedule_1_text.place(x=85, y=800)
        schedule_2_text.place(x=205, y=800)
        schedule_3_text.place(x=325, y=800)
        schedule_confirm.place(x=170, y=850)

        ok_button.place(x=1000, y=900)

class SborPlushekSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'
        def set_defaul_click_in_clan_SborPlushek():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'SborPlushek_amount_of_clicks_in_clan' in i:
                        amount_of_clicks = i.split('=')[1]
                        amount_of_clicks_in_clan_text.insert(-1,amount_of_clicks)
                        print(i)
                        break

        def set_SborPlushek_click_in_clan():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'SborPlushek_amount_of_clicks_in_clan' in i:
                        amount_of_clicks = i.split('=')
                        print(i)
                        break

                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(amount_of_clicks[1])
                    amount_of_clicks_for_set = amount_of_clicks_in_clan_text.get()
                    new_data = old_data.replace(i, f'SborPlushek_amount_of_clicks_in_clan={amount_of_clicks_for_set}\n')
                with open ('settings.txt', 'w') as f:
                    f.write(new_data)

                print(123)

        def set_defaul_schedule_SborPlushek():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'SborPlushek_schedule' in i:
                        schedule_list = i.split('=')[1]
                        schedule = schedule_list.split(',')
                        schedule_1_text.insert(-1, schedule[0].replace('(', '').replace(')', ''))
                        print(i)
                        break

        def set_SborPlushek_schedule():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'SborPlushek_schedule' in i:
                        price = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(price[1])
                    schedule_data = []
                    schedule_data.append(schedule_1_text.get().replace(' ', '').replace('\n', ''))

                    new_data = old_data.replace(i, f'SborPlushek_schedule=({"".join(schedule_data)})\n')

                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)

        amount_of_clicks_in_clan = tk.Label(self, text='Количество сборов в клане', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        amount_of_clicks_in_clan_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 32', justify='center')
        amount_of_clicks_in_clan_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0,command=set_SborPlushek_click_in_clan)

        schedule = tk.Label(self, text='Расписание', bg='#282828', fg='#d4d3d3',font='Arial 24',borderwidth=0)
        schedule_1 = tk.Label(self, text='Время 1:', bg='#282828', fg='#d4d3d3',font='Arial 32',borderwidth=0)

        schedule_1_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 32', justify='center')
        schedule_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0,command=set_SborPlushek_schedule)
        ok_button = tk.Button(self, text='Ок ', height=1, width=8, bg='#535353', fg='#d4d3d3',font='Arial 24',borderwidth=0, command=lambda: controller.show_frame('AllBots'))
        set_defaul_schedule_SborPlushek()
        set_defaul_click_in_clan_SborPlushek()
        ok_button.bind('<Enter>', lambda event, h=ok_button: con(h, '#404040'))
        ok_button.bind("<Leave>", lambda event, h=ok_button: con(h, "#535353"))

        amount_of_clicks_in_clan.place(x=100,y=400)
        amount_of_clicks_in_clan_text.place(x=200, y=450)
        amount_of_clicks_in_clan_confirm.place(x=200,y=550)
        schedule.place(x=800, y=200)
        schedule_1.place(x=700, y=300)

        schedule_1_text.place(x=900, y=300)

        schedule_confirm.place(x=800, y=700)

        ok_button.place(x=1000, y=900)


class AutoSellSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'
        def set_defaul_schedule_AutoSell():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'AutoSell_schedule' in i:
                        schedule_list = i.split('=')[1]
                        schedule = schedule_list.split(',')
                        schedule_1_text.insert(-1, schedule[0].replace('(', '').replace(' ', ''))
                        schedule_2_text.insert(-1, schedule[1].replace(' ', ''))
                        schedule_3_text.insert(-1, schedule[2].replace(')', '').replace(' ', ''))
                        print(i)
                        break

        def set_AutoSell_schedule():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'AutoSell_schedule' in i:
                        price = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(price[1])
                    schedule_data = []
                    schedule_data.append(schedule_1_text.get().replace(' ', '') + ', ')
                    schedule_data.append(schedule_2_text.get().replace(' ', '') + ', ')
                    schedule_data.append(schedule_3_text.get().replace(' ', '').replace('\n', ''))
                    new_data = old_data.replace(i, f'AutoSell_schedule=({"".join(schedule_data)})\n')

                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)

        schedule = tk.Label(self, text='Расписание', bg='#282828', fg='#d4d3d3',font='Arial 24',borderwidth=0)
        schedule_1 = tk.Label(self, text='Время 1:', bg='#282828', fg='#d4d3d3',font='Arial 32',borderwidth=0)
        schedule_2 = tk.Label(self, text='Время 2:', bg='#282828', fg='#d4d3d3',font='Arial 32',borderwidth=0)
        schedule_3 = tk.Label(self, text='Время 3:', bg='#282828', fg='#d4d3d3',font='Arial 32',borderwidth=0)
        schedule_1_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 32', justify='center')
        schedule_2_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 32', justify='center')
        schedule_3_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 32', justify='center')
        schedule_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0,command=set_AutoSell_schedule)
        ok_button = tk.Button(self, text='Ок ', height=1, width=8, bg='#535353', fg='#d4d3d3',font='Arial 24',borderwidth=0, command=lambda: controller.show_frame('AllBots'))
        set_defaul_schedule_AutoSell()

        ok_button.bind('<Enter>', lambda event, h=ok_button: con(h, '#404040'))
        ok_button.bind("<Leave>", lambda event, h=ok_button: con(h, "#535353"))

        schedule.place(x=600, y=200)
        schedule_1.place(x=500, y=300)
        schedule_2.place(x=500, y=450)
        schedule_3.place(x=500, y=600)
        schedule_1_text.place(x=700, y=300)
        schedule_2_text.place(x=700, y=450)
        schedule_3_text.place(x=700, y=600)
        schedule_confirm.place(x=600, y=700)

        ok_button.place(x=1000, y=900)

class GreenCheckSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'

        def set_defaul_mode():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'GreenCheck_mode' in i:
                        default_mode = i.split('=')[1]
                        mode_text.insert(-1, default_mode.replace(' ', ''))
                        print(i)
                        break
        def set_mode():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'GreenCheck_mode' in i:
                        price = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(price[1])
                    mode = mode_text.get()
                    new_data = old_data.replace(i, f'GreenCheck_mode={mode}\n')

                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)


        def set_defaul_hotkey():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'GreenCheck_hotkey' in i:
                        default_hotkey = i.split('=')[1]
                        hotkey_text.insert(-1, default_hotkey.replace(' ', ''))
                        print(i)
                        break
        def set_hotkey():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'GreenCheck_hotkey' in i:
                        price = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(price[1])
                    hotkey = hotkey_text.get()
                    new_data = old_data.replace(i, f'GreenCheck_hotkey={hotkey}')

                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)




        hotkey = tk.Label(self, text='Хоткей', bg='#282828', fg='#d4d3d3',font='Arial 46',borderwidth=0)
        hotkey_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 40', justify='center')
        hotkey_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_hotkey)

        mode = tk.Label(self, text='Режим', bg='#282828', fg='#d4d3d3',font='Arial 46',borderwidth=0)
        mode_text = tk.Entry(self, width=8,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 40', justify='center')
        mode_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_mode)

        ok_button = tk.Button(self, text='Ок ', height=1, width=8, bg='#535353', fg='#d4d3d3',font='Arial 24',borderwidth=0, command=lambda: controller.show_frame('AllBots'))

        set_defaul_hotkey()
        set_defaul_mode()

        hotkey.place(x=550, y=200)
        hotkey_text.place(x=530, y=300)
        hotkey_confirm.place(x=560, y=400)

        mode.place(x=550, y=500)
        mode_text.place(x=530, y=600)
        mode_confirm.place(x=560, y=700)


        ok_button.place(x=1000, y=900)

class MainSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'
        def set_defaul_path():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'path' in i:
                        tg_id_new = i.split('=')[1]
                        path_text.insert(-1, tg_id_new.replace(' ', ''))
                        print(i)
                        break

        def set_path():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'path' in i:
                        price = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(price[1])
                    hotkey = path_text.get()
                    new_data = old_data.replace(i, f'path={hotkey}')
                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)

        def set_defaul_tg_id():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'tg_id' in i:
                        tg_id_new = i.split('=')[1]
                        tg_id_text.insert(-1, tg_id_new.replace(' ', ''))
                        print(i)
                        break

        def set_tg_id():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'tg_id' in i:
                        price = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(price[1])
                    hotkey = multiplier_text.get()
                    new_data = old_data.replace(i, f'tg_id={hotkey}')
                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)


        def set_defaul_multiplier():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'multiplier' in i:
                        default_hotkey = i.split('=')[1]
                        multiplier_text.insert(-1, default_hotkey.replace(' ', ''))
                        print(i)
                        break

        def set_multiplier():
            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'multiplier' in i:
                        price = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(price[1])
                    hotkey = multiplier_text.get()
                    new_data = old_data.replace(i, f'multiplier={hotkey}')
                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)

        go_to_all_bots = tk.Button(self, text="Все боты" ,background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth=0, compound='center',font='Arial 24', command=lambda: controller.show_frame('AllBots'))
        go_to_main = tk.Button(self, text="Главная", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center', font='Arial 24', command=lambda: controller.show_frame('Main'))
        go_to_settings = tk.Button(self, text="Настройки", background='#535353', fg='#d4d3d3', height=2, width=23, borderwidth = 0, compound='center',font='Arial 24')

        go_to_all_bots.bind('<Enter>', lambda event, h=go_to_all_bots: con(h, '#404040'))
        go_to_all_bots.bind("<Leave>", lambda event, h=go_to_all_bots: con(h, "#535353"))
        go_to_main.bind('<Enter>', lambda event, h=go_to_main:con(h, '#404040'))
        go_to_main.bind("<Leave>", lambda event, h=go_to_main: con(h, "#535353"))
        go_to_settings.bind('<Enter>', lambda event, h=go_to_settings: con(h, '#404040'))
        go_to_settings.bind("<Leave>", lambda event, h=go_to_settings: con(h, "#535353"))

        multiplier = tk.Label(self, text='Множитель задержки', bg='#282828', fg='#d4d3d3',font='Arial 24',borderwidth=0)
        multiplier_text = tk.Entry(self, width=17,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 24', justify='center')
        multiplier_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_multiplier)

        tg_id = tk.Label(self, text='Telegram ID', bg='#282828', fg='#d4d3d3',font='Arial 24',borderwidth=0)
        tg_id_text = tk.Entry(self, width=17,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 24', justify='center')
        tg_id_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_defaul_tg_id)

        path = tk.Label(self, text='Путь до проекта', bg='#282828', fg='#d4d3d3',font='Arial 24',borderwidth=0)
        path_text = tk.Entry(self, width=17,borderwidth=0, bg='#535353',fg='#5ecb41', font='Arial 24', )
        path_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_path)

        main_bots = tk.Label(self, text='Боты для запуска одной кнопкой', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        buyer_bot = tk.Label(self, text='Скупщик', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        sborplushek_bot = tk.Label(self, text='Сбор плюшек', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)
        autosell_bot = tk.Label(self, text='Автоперестановка', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)

        buyer_bot_checkbutton = tk.Button(self, text='Скупщик', width=19, bg='#535353', fg='#5ecb41',font='Arial 32',borderwidth=0)
        sborplushek_bot_checkbutton = tk.Button(self, text='Сборщик плюшек', width=19, bg='#535353', fg='#5ecb41',font='Arial 32',borderwidth=0)
        autosell_bot_checkbutton = tk.Button(self, text='Автоперестановка', width=19, bg='#535353', fg='#5ecb41',font='Arial 32',borderwidth=0)

        set_defaul_multiplier()
        set_defaul_tg_id()
        set_defaul_path()

        multiplier.place(x=100, y=200)
        multiplier_text.place(x=105,y=250)
        multiplier_confirm.place(x=160, y=300)

        tg_id.place(x=170,y=400)
        tg_id_text.place(x=100,y=450)
        tg_id_confirm.place(x=160, y=500)

        path.place(x=135, y=600)
        path_text.place(x=100, y=650)
        path_confirm.place(x=160, y=700)

        main_bots.place(x=700, y=200)
        buyer_bot_checkbutton.place(x=700, y=300)
        sborplushek_bot_checkbutton.place(x=700, y=400)
        autosell_bot_checkbutton.place(x=700, y=500)

        go_to_all_bots.place(x=0, y=0)
        go_to_main.place(x=430, y=0)
        go_to_settings.place(x=860, y=0)


class BotForStatSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'

        def set_stats_for_armor():

            list_of_stat = {}

            first_stat = first_stat_combobox.get()
            first_value = first_value_combobox.get()

            second_stat = second_stat_combobox.get()
            second_value = second_value_combobox.get()

            third_stat = third_stat_combobox.get()
            third_value = third_value_combobox.get()

            list_of_stat[first_stat] = first_value
            list_of_stat[second_stat] = second_value
            list_of_stat[third_stat] = third_value

            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BotForStat_statlist' in i:
                        stat = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(stat[1])
                    new_data = old_data.replace(i, f'BotForStat_statlist={str(list_of_stat)}\n')
                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)

        def set_stats_for_accesories():

            list_of_stat = {}

            first_stat = first_stat_for_acessories_combobox.get()
            first_value = first_value_for_acessories_combobox.get()

            second_stat = second_stat_for_acessories_combobox.get()
            second_value = second_value_for_acessories_combobox.get()

            third_stat = third_stat_for_acessories_combobox.get()
            third_value = third_value_for_acessories_combobox.get()

            list_of_stat[first_stat] = first_value
            list_of_stat[second_stat] = second_value
            list_of_stat[third_stat] = third_value

            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BotForStat_statlist' in i:
                        stat = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(stat[1])
                    new_data = old_data.replace(i, f'BotForStat_statlist={str(list_of_stat)}\n')
                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)



        def set_stats_for_weapon():

            list_of_stat = {}

            first_stat = first_stat_for_weapon_combobox.get()
            first_value = first_value_for_weapon_combobox.get()

            second_stat = second_stat_for_weapon_combobox.get()
            second_value = second_value_for_weapon_combobox.get()

            third_stat = third_stat_for_weapon_combobox.get()
            third_value = third_value_for_weapon_combobox.get()

            list_of_stat[first_stat] = first_value
            list_of_stat[second_stat] = second_value
            list_of_stat[third_stat] = third_value

            with open('settings.txt') as f:
                for i in f.readlines():
                    if 'BotForStat_statlist' in i:
                        stat = i.split('=')
                        print(i)
                        break
                with open ('settings.txt', 'r') as f:
                    old_data = f.read()
                    print(stat[1])
                    new_data = old_data.replace(i, f'BotForStat_statlist={str(list_of_stat)}\n')
                with open ('settings.txt', 'w') as f:
                    f.write(new_data)
                print(123)

        def set_default_stats():
            pass

        FIRST_STATS_LIST = [
            'Ничего',
            'Макс. НР',
            'Макс. МР',
            'Восстановление НР (период)',
            'Восстановление МР (Период)',
            'Сопр. Крит. Атк. в Ближн. бою',
            'Сопр. Крит. Атк. в дальн. бою',
            'Сопротивление Маг. Крит. Атк.',
            'Защита'
        ]

        SECOND_STATS_LIST = (
            'Ничего',
            'Защита',
            'Сопротивление умениям',
            'Снижение урона',
            'Уклонение в ближн. бою',
            'Уклонение в дальн. бою',
            'Маг. Уклонение',
            'Макс грузоподъемность',
        )

        THIRD_STATS_LIST = (
            'Ничего',
            'СИЛ',
            'ЛВК',
            'ИНТ',
            'ВЫН',
            'ПРВ',
            'МДР',
        )

        FIRST_STATS_LIST_FOR_WEAPON = (
            'Ничего',
            'Урон от оружия',
            'Точность',
            'Крит. Атк.',
            'Доп урон Крит. Атк.',
            'Шанс двойного урона',
            'Макс. НР',
            'Макс. МР'
        )

        SECOND_STATS_LIST_FOR_WEAPON = (
            'Ничего',
            'Урон водой',
            'Урон огнем',
            'Урон ветром',
            'Урон землей',
            'Урон святостью',
            'Урон тьмой'
        )

        THIRD_STATS_LIST_FOR_WEAPON = (
            'Ничего',
            'Увелечение урона от оружия',
            'Точность',
            'Доп. Урон',
        )

        FIRST_STATS_LIST_FOR_ACESSORIES = (
            'Ничего',
            'Макс. НР',
            'Макс. МР',
            'Восстановление НР (период)',
            'Восстановление МР (Период)',
            'Сопр. Крит. Атк. в Ближн. бою',
            'Сопр. Крит. Атк. в дальн. бою',
            'Сопротивление Маг. Крит. Атк.',
            'Защита',
            'Урон от оружия',
            'Точность',
            'Крит. Атк.',
            'Доп урон Крит. Атк.',
            'Шанс двойного урона'
        )

        SECOND_STATS_LIST_FOR_ACESSORIES = (
            'Ничего',
            'Защита',
            'Сопротивление умениям',
            'Снижение урона',
            'Уклонение в ближн. бою',
            'Уклонение в дальн. бою',
            'Маг. Уклонение',
            'Макс грузоподъемность',
            'Урон водой',
            'Урон огнем',
            'Урон ветром',
            'Урон землей',
            'Урон святостью',
            'Урон тьмой'

        )

        THIRD_STATS_LIST_FOR_ACCESORIES = (
            'Ничего',
            'СИЛ',
            'ЛВК',
            'ИНТ',
            'ВЫН',
            'ПРВ',
            'МДР',
            'Увелечение урона от оружия',
            'Точность',
            'Доп. Урон'
        )

        VALUE_LIST = (
            'Ничего',
            '+1',
            '+2',
            '+3',
            '+1%',
            '+2%',
            '+3%',
            '+4%',
            '+5%',
            '+10',
            '+20',
            '+30',
            '+40',
            '+50',
            '+60',
            '+70',
            '+80',
        )
        armor_label = tk.Label(self, text='Статы для брони', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)

        first_stat_label = tk.Label(self, text='1 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        first_stat_combobox = ttk.Combobox(self, values=FIRST_STATS_LIST, font='Arial 20')

        second_stat_label = tk.Label(self, text='2 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        second_stat_combobox = ttk.Combobox(self, values=SECOND_STATS_LIST, font='Arial 20')

        third_stat_label = tk.Label(self, text='3 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        third_stat_combobox = ttk.Combobox(self, values=THIRD_STATS_LIST, font='Arial 20')

        first_value_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')
        second_value_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')
        third_value_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')

        armor_stats_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_stats_for_armor)


        accesories_label = tk.Label(self, text='Статы для бижи', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)

        first_stat_for_acessories_label = tk.Label(self, text='1 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        first_stat_for_acessories_combobox = ttk.Combobox(self, values=FIRST_STATS_LIST_FOR_ACESSORIES, font='Arial 20')

        second_stat_for_acessories_label = tk.Label(self, text='2 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        second_stat_for_acessories_combobox = ttk.Combobox(self, values=SECOND_STATS_LIST_FOR_ACESSORIES, font='Arial 20')

        third_stat_for_acessories_label = tk.Label(self, text='3 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        third_stat_for_acessories_combobox = ttk.Combobox(self, values=THIRD_STATS_LIST_FOR_ACCESORIES, font='Arial 20')

        first_value_for_acessories_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')
        second_value_for_acessories_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')
        third_value_for_acessories_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')

        accesories_stats_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_stats_for_accesories)


        weapon_label = tk.Label(self, text='Статы для оружия', bg='#282828', fg='#d4d3d3',font='Arial 24', borderwidth=0)

        first_stat_for_weapon_label = tk.Label(self, text='1 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        first_stat_for_weapon_combobox = ttk.Combobox(self, values=FIRST_STATS_LIST_FOR_WEAPON, font='Arial 20')

        second_stat_for_weapon_label = tk.Label(self, text='2 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        second_stat_for_weapon_combobox = ttk.Combobox(self, values=SECOND_STATS_LIST_FOR_WEAPON, font='Arial 20')

        third_stat_for_weapon_label = tk.Label(self, text='3 стат', bg='#282828', fg='#d4d3d3',font='Arial 20', borderwidth=0)
        third_stat_for_weapon_combobox = ttk.Combobox(self, values=THIRD_STATS_LIST_FOR_WEAPON, font='Arial 20')

        first_value_for_weapon_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')
        second_value_for_weapon_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')
        third_value_for_weapon_combobox = ttk.Combobox(self, values=VALUE_LIST, font='Arial 20')

        weapon_stats_confirm = tk.Button(self, text='Подтвердить', height=1, width=11, bg='#535353', fg='#5ecb41',font='Arial 20',borderwidth=0, command=set_stats_for_weapon)

        set_default_stats()


        armor_label.place(x=170, y=100)

        first_stat_label.place(x=100, y=250)
        first_stat_combobox.place(x=100, y=300)
        first_value_combobox.place(x=100, y=350)

        second_stat_label.place(x=100, y=450)
        second_stat_combobox.place(x=100, y=500)
        second_value_combobox.place(x=100, y=550)

        third_stat_label.place(x=100, y=650)
        third_stat_combobox.place(x=100, y=700)
        third_value_combobox.place(x=100, y=750)

        armor_stats_confirm.place(x=200, y=850)


        accesories_label.place(x=500, y=100)

        first_stat_for_acessories_label.place(x=450, y=250)
        first_stat_for_acessories_combobox.place(x=450, y=300)
        first_value_for_acessories_combobox.place(x=450, y=350)

        second_stat_for_acessories_label.place(x=450, y=450)
        second_stat_for_acessories_combobox.place(x=450, y=500)
        second_value_for_acessories_combobox.place(x=450, y=550)

        third_stat_for_acessories_label.place(x=450, y=650)
        third_stat_for_acessories_combobox.place(x=450, y=700)
        third_value_for_acessories_combobox.place(x=450, y=750)

        accesories_stats_confirm.place(x=500, y=850)


        weapon_label.place(x=850, y=100)

        first_stat_for_weapon_label.place(x=800, y=250)
        first_stat_for_weapon_combobox.place(x=800, y=300)
        first_value_for_weapon_combobox.place(x=800, y=350)

        second_stat_for_weapon_label.place(x=800, y=450)
        second_stat_for_weapon_combobox.place(x=800, y=500)
        second_value_for_weapon_combobox.place(x=800, y=550)

        third_stat_for_weapon_label.place(x=800, y=650)
        third_stat_for_weapon_combobox.place(x=800, y=700)
        third_value_for_weapon_combobox.place(x=800, y=750)
        
        weapon_stats_confirm.place(x=850, y=850)



        ok_button = tk.Button(self, text='Ок ', height=1, width=8, bg='#535353', fg='#d4d3d3',font='Arial 24', borderwidth=0, command=lambda: controller.show_frame('AllBotsSecondPage'))
        ok_button.place(x=1000, y=900)

class AlchemySettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = '#282828'

        with open('alchemy_account_preset.txt', 'r', encoding='utf-8') as accounts_presets_text:
            accounts_presets = accounts_presets_text.read()
        acc_names = []
        acc_rolls = []
        amount_rolls_for_each_acc = []

        accs_colors = []

        for i in accounts_presets.split('\n'):
            if i == '':
                continue
            acc_info = i.split(' ')
            print(acc_info)
            acc_name = tk.Label(self, text=acc_info[0], bg='#282828', fg='#d4d3d3', font='Arial 12', borderwidth=0)

            acc_roll = ttk.Combobox(self, values=LIST_OF_ROLLS, font='Arial 12')
            acc_roll.set(acc_info[1])

            amount_of_rolls = tk.Entry(self, bg='#535353', fg='#d4d3d3', font='Arial 12', borderwidth=0)
            amount_of_rolls.insert(0, acc_info[-2])

            acc_colors = tk.Entry(self, bg='#282828', font='Arial 12', fg='#5ecb41')

            acc_names.append(acc_name)
            acc_rolls.append(acc_roll)
            amount_rolls_for_each_acc.append(amount_of_rolls)

            accs_colors.append(acc_colors)

        def get_acc_list():
            acc_names_list = AlchemyBot.get_accs_names()
            acc_names_list_labels = []

            string_to_file = ''
            for i in acc_names_list:
                string_to_file += i
                string_to_file += ' Roll_00'
                string_to_file += ' 1' + '\n'
            with open('alchemy_account_preset.txt', 'w', encoding='utf-8') as acc_presets_text:
                acc_presets_text.write(string_to_file)
                print('Данные об аккаунтах получены и записаны')

        def update_account_presets():
            string_to_file = ''
            for i in range(len(accounts_presets.split('\n'))):
                print(i)
                try:
                    string_to_file += acc_names[i]['text'] + ' '
                    string_to_file += acc_rolls[i].get() + ' '
                    string_to_file += amount_rolls_for_each_acc[i].get() + ' '
                    string_to_file += accs_colors[i].get().replace(' ', '').upper() + '\n'
                    with open('alchemy_account_preset.txt', 'w', encoding='utf-8') as acc_presets_text:
                        acc_presets_text.write(string_to_file)
                except:
                    pass
        counter = 0
        for i in acc_names:
            i.place(x=50, y=100+counter)
            counter += 50
        counter = 0
        for i in acc_rolls:
            i.place(x=200, y=100+counter)
            counter += 50
        counter = 0
        for i in amount_rolls_for_each_acc:
            i.place(x=500, y=100+counter)
            counter += 50

        counter = 0
        for i in accs_colors:
            i.place(x=800, y=100+counter)
            counter += 50

        update_button = tk.Button(self, text='Обновить список акков', height=1, width=20, bg='#535353', fg='#d4d3d3',font='Arial 24', borderwidth=0, command=get_acc_list)

        ok_button = tk.Button(self, text='Ок ', height=1, width=8, bg='#535353', fg='#d4d3d3',font='Arial 24', borderwidth=0, command=lambda: controller.show_frame('AllBotsSecondPage'))

        confirm_button = tk.Button(self, text='Подтвердить', height=1, width=20, bg='#535353', fg='#d4d3d3',font='Arial 24', borderwidth=0, command=update_account_presets)

        ok_button.place(x=800, y=800)
        update_button.place(x=800, y=600)

        confirm_button.place(x=800, y=400)

if __name__ == '__main__':
    app = SampleApp()
    app.mainloop()

#time.sleep(6)
#
#cases_bot.main()

