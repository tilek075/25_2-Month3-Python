from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import dp, bot


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


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(send_mem, commands=['mem'])
