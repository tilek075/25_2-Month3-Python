import random
from typing import List

from aiogram import types, Dispatcher
from config import bot


from config import ADMINS


async def echo(message: types.Message):
    if message.text.lower().startswith('game'):
        if message.from_user.id not in ADMINS:
            await message.answer("Функция только для администратора")
        else:
            emoji_list = ["⚽", "🎲", "🏀", "🎳", "🎯", "🎰"]
            emoji_send = random.choice(emoji_list)
            await bot.send_dice(message.chat.id, emoji=emoji_send)
    elif not message.text.isdigit():
        await message.answer(message.text)
    else:
        await message.answer(f'{int(message.text) ** 2}')


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(echo)

