from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS
from keyboards import client_kb
from random import randint


class FSMAdmin(StatesGroup):
    id = State()
    name = State()
    age = State()
    direction = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private" and message.from_user.id in ADMINS:
        await FSMAdmin.name.set()
        await message.answer("Введите имя ментора", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Доступно только в ЛС для администратора бота!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = randint(10000, 99999)
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Укажите возраст ментора")


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Только числа!")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Какое направление?")


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Укажите группу", reply_markup=client_kb.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
        await message.answer(
            f"Данные ментора:\n{data['id']},\n{data['name']},\n{data['age']},\n{data['direction']},"
            f"\n{data['group']}"
        )
    await FSMAdmin.next()
    await message.answer("Все верно?", reply_markup=client_kb.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.finish()
    elif message.text.lower() == "заново":
        await FSMAdmin.name.set()
        await message.answer("Имя ментора?")
    else:
        await message.answer('Ошибка!')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Canceled")


def register_handlers_anket(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_reg,
                                Text(equals="cancel", ignore_case=True),
                                state="*")
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
