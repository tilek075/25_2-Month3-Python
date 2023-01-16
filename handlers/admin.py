from aiogram import types, Dispatcher
from config import dp, ADMINS, bot


@dp.message_handler(commands='!pin')
async def pin_message(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer("Функция только для администратора")
        elif not message.reply_to_message:
            await message.answer("Выберите сообщение для закрепления!")
        else:
            await bot.pin_chat_message(message.chat.id, message.message_id)

    else:
        await message.answer("Пиши в группе!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(pin_message, commands=['!pin'])
