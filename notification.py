import asyncio
from aiogram import types, Dispatcher
from config import bot
from datetime import datetime
import schedule


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = []
    chat_id.append(message.from_user.id)
    await message.answer("Ok")


async def begin_study():
    for id_user in chat_id:
        await bot.send_message(id_user, "Начинается урок")


async def scheduler():
    schedule.every().hours.until(datetime(2023, 1, 26, 20, 00)).do(begin_study)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def register_handler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id, lambda word: "Напомнить" in word.text)
