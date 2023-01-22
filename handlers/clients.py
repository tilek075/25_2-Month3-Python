from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import dp, bot, ADMINS
from database.bot_db import sql_command_random, sql_command_delete


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await message.answer(f"Hi, {message.from_user.first_name}!!!")


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)

    question = "Столица Португалии?"
    answers = [
        "Мадрид",
        "Мадейра",
        "Рим",
        "Лиссабон",
        "Осло"
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="Столица Португалии - Лиссабон",
        open_period=60,
        reply_markup=markup
    )


@dp.message_handler(commands=['mem'])
async def send_mem(message: types.Message):
    await message.answer_photo(photo=open("media/2.jpg", 'rb'))


async def get_random_user(message: types.Message):
    random_user = await sql_command_random()
    markup = None
    if message.from_user.id in ADMINS:
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(f"delete {random_user[1]}",
                                 callback_data=f"delete {random_user[0]}"))
    await message.answer(f"{random_user[1]} {random_user[2]} {random_user[3]} {random_user[4]}",
                         reply_markup=markup)


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Deleted!", show_alert=True)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(send_mem, commands=['mem'])
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_callback_query_handler(complete_delete, lambda call: call.data and call.data.startswith("delete "))