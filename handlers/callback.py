from aiogram import types, Dispatcher
from config import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.callback_query_handler(text="button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_2 = InlineKeyboardButton("NEXT", callback_data='button_call_2')
    markup.add(button_call_2)
    question = "Флаг какой страны изображен на картинке?"
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
        reply_markup=markup
    )


@dp.callback_query_handler(text="button_call_2")
async def quiz_3(call: types.CallbackQuery):
    question = "В какой стране находится гора Эверест?"
    answers = [
        'Индия',
        'Китай',
        'Индонезия',
        'Япония',
        'Непал',
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        explanation="Непал",
        open_period=60,
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text="button_call_1")
