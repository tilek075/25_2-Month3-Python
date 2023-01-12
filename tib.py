from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from decouple import config
import logging

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


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


@dp.callback_query_handler(text="button_call_1")
async def quiz_2(call: types.CallbackQuery):
    question = "Флаг какой страны изображен на картинке?!"
    answers = [
        'Великобритания',
        'Новая Зеландия',
        'Австралия',
        'Бельгия',
        'Бразилия',
    ]

    photo = open("media/1.jpg", 'rb')
    await bot.send_photo(call.from_user.id, photo=photo)

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Флаг Новой Зеландии",
        open_period=60,
    )


@dp.message_handler(commands=['mem'])
async def send_mem(message: types.Message):
    await message.answer_photo(photo=open("media/2.jpg", 'rb'))


@dp.message_handler()
async def echo(message: types.Message):
    if not message.text.isdigit():
        await bot.send_message(message.from_user.id, message.text)
    else:
        await bot.send_message(message.from_user.id, f'{message.text ** 2}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)