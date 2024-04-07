import asyncio
import os
import random
import time
import json
import nest_asyncio

from telethon import types, functions
from telethon.sync import TelegramClient

nest_asyncio.apply()


class Viever:
    """Класс для просмотра историй"""
    def __init__(self, api_id, api_hash, phone_number, code):
        self.api_id, self.api_hash = api_id, api_hash
        self.LIMIT = LIMIT
        self.emoji = ['❤️', '👍', '🥰', '🔥', '👏', '😁']
        self.client = TelegramClient(phone_number, self.api_id, self.api_hash, system_version="4.16.30-vxCUSTOM")
        self.phone_number = phone_number

    async def send_code(self):
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)

    async def get_code(self, code):
        await self.client.sign_in(self.phone_number, code)

    async def connect(self, code):
        #Сюда добавил code. Который можно передать из тг
        """Класс для подключения к акку"""
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, code)

        await self.client.start()
        await self.main()

    async def disconnect(self):
        """Класс для дисконекта от акка"""
        await self.client.disconnect()

    async def get_users_if_list_of_participants_is_not_availible(self, dialog):
        """Класс для поиска и просмотра историй если список участников в беседе скрыт"""
        users_two = []
        partisipants = {}
        count = 0

        entity = await self.client.get_entity(dialog)
        async for message in self.client.iter_messages(entity.id, limit=self.LIMIT):
            try:
                sender = await message.get_sender()
                if sender is None:
                    continue
                partisipants.update({sender.username: sender})
            except:
                continue

        for user, sender in partisipants.items():
            try:
                if not sender.stories_unavailable and not sender.stories_hidden and sender.stories_max_id:
                   await self.client(functions.stories.ReadStoriesRequest(peer=sender.id, max_id=sender.stories_max_id))
                   await self.client(functions.stories.SendReactionRequest(peer=sender.id, story_id=sender.stories_max_id, reaction=types.ReactionEmoji(emoticon=random.choice(self.emoji))))

                   users_two.append(f'{sender.id}, {sender.username}')
                   count += 1

            except Exception as e:
                print(e)
                continue

        return users_two, count

    async def get_users_if_list_of_participants_availible(self):
        """Класс для поиска и просмотра историй если список участников в беседе не скрыт"""
        users_one = []
        file_name = None

        dialogs = await self.client.get_dialogs()
        for dialog in dialogs:
            try:
                count = 0
                if dialog.is_group:
                    entity = await self.client.get_entity(dialog)
                    time.sleep(1) #Зачем тут таймслип?
                    if dialog.entity.participants_count == len([i async for i in self.client.iter_participants(entity=dialog.entity)]):
                        async for user in self.client.iter_participants(entity=dialog.entity):
                            if not user.stories_unavailable and not user.stories_hidden and user.stories_max_id:
                                await self.client(functions.stories.ReadStoriesRequest(peer=user.id, max_id=user.stories_max_id))
                                await self.client(functions.stories.SendReactionRequest(peer=user.id, story_id=user.stories_max_id, reaction=types.ReactionEmoji(emoticon=random.choice(self.emoji))))

                                users_one.append(f'{user.id}, {user.username}, {user.phone_number}')
                                count += 1
                    else:
                        func, vievs = await self.get_users_if_list_of_participants_is_not_availible(dialog)
                        users_one.append('\n'.join(func))
                        count += vievs
                    text = f'В группе {entity.title} просмотренно пользователей {count}'
                file_name = f'number of views from the phone {self.phone_number}.txt'
            except:
                continue
        return list(set(users_one)), file_name, text

    async def write_unique_elements(self, file_name, users):
        """Функция для записи всех айдишников и ников полученных при просмотре историй
        через set для исключения дубликатов"""
        if not os.path.exists(file_name):
            open(file_name, 'w').close()

        with open(file_name, 'r+') as file:
            previous_elements = file.read().splitlines()
            unique_elements = set(users).difference(set(previous_elements))
            if unique_elements and unique_elements not in previous_elements:
                file.seek(0, 2)
                file.write('\n'.join(unique_elements) + '\n')
                #file.close() close в with не нужен. With делает это сам
            #else:
            #    file.close()
            #Тут тоже самое

        with open(file_name, "r") as file:
            lines = file.readlines()

        unique_lines = []
        for line in lines:
            if line not in unique_lines:
                unique_lines.append(line)

        with open(file_name, "w") as file:
            for line in unique_lines:
                file.write(line)

    async def main(self):
        """Основной метод запуска программы"""
        print('Переходим на следуюший аккаунт')

        users, file_name = await self.get_users_if_list_of_participants_availible()
        await self.write_unique_elements(file_name, users)
        await self.write_unique_elements('all_users.txt', users)
        await self.disconnect()

with open("Settings.json", 'r', encoding='utf-8') as settings:
    settings_data = json.load(settings)

#Рекомендую сделать api_id и api_hash конастантами. Ибо в процеесе программы они меняться не будут
api_id, api_hash = settings_data.get("api_id"), settings_data.get("api_hash")
phone_numbers = [i for i in settings_data.get("PHONE_NUMBERS")]
LIMIT = settings_data.get("limit")

clients = []

init = Init()

async def run(code):
    """Функция запуска программы"""
    for phone_number in phone_numbers:
        client = Viever(api_id, api_hash, phone_number, code)
        clients.append(client)

        await client.connect()

async def launch():
    #на будущее. Лучше не делай run и launch в одном файле)
    #Так же у тебя вызывается только метод connect.
    #Хотя он делает грубо говоря всю магию. В будущих проектах лучше создавай основню работу проги в main,
    #а в методы по типу connect только подлкючение
    while True:
        asyncio.run(run())
        time.sleep(random.randint(15, 30))

