from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import asyncio
from asyncio import new_event_loop

import threading
import multiprocessing
import json
import viever
import time
import random

#методы которые не используются лучше убирать после разработки. Ну это я уже просто доебываюсь) Красава на мамом деле, прям неплохо код читется
with open("Settings.json", 'r', encoding='utf-8') as settings:
    settings_data = json.load(settings)

TOKEN = settings_data.get("TOKEN")
dp = Dispatcher()

@dp.message(CommandStart())
#тут -> обязательный?
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}, {message.from_user.id}!")
    #лучше вынести TG_ID в отдельную переменную
    if message.from_user.id == 6752793212:
        await message.answer("Команды всего две \n /launch и /stop")

@dp.message(F.text == '/codes')
async def send_code_for_accounts():
    for phone_number in phone_numbers:
        client = viever.Viever('Сюда всю хуйню прописать нада')
        await client.send_code()

#Нужно сделать чтобы эта функция вызывалась когда приходит ответ на функцию выше
async def get_code_for_account(code):
    code = int(code)
    client = viever.Viever('Сюда всю хуйню прописать нада')
    await client.get_code(code)

@dp.message(F.text == '/launch')
async def launch_program(message: Message):
    #await message.answer(viever.run)
    #watch_stories = viever.run

    #start = asyncio.ensure_future(viever.launch())
    #await message.answer('Введите код пришедший на номер ')
    #num = int(message.text)
    #reg = asyncio.ensure_future(viever.connect())
    #await message.answer(f'{viever}')
    asyncio.run(viever.run)

#@dp.message(F.text == 'stop')
#async def stop_program(message: Message):
#    disconect = await viever.Viever.disconnect()

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    #await dp.start_polling(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
    loop.run_forever()

if __name__ == "__main__":
   asyncio.run(main())