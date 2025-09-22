from aiogram import Router, html
import asyncio
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from lexicon import *
from python_db import users_db
from postgress_functions import (check_user_in_table, insert_new_user_in_table,
                            get_user_count,  return_orders, return_tg_id)
from bot_instance import FSM_ST, dp, bot_storage_key, server_cart
from keyboards import show_my_orders_kb
from filters import SHOW_BUTTON, IS_ADMIN
from aiogram.exceptions import TelegramForbiddenError
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
import json


ch_router = Router()

@ch_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    if not await check_user_in_table(user_id):
        print(message.from_user.id)

        await state.set_state(FSM_ST.after_start)
        await insert_new_user_in_table(user_id, user_name)
        bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
        bot_dict[str(user_id)] = {'name':user_name, 'order':{}}  # Создаю пустой словарь для заметок юзера

        await dp.storage.update_data(key=bot_storage_key, data=bot_dict)  # Обновляю словарь бота

        insgesamt = await get_user_count() # Получаю общее количество уже запустивших бота

        server_cart[user_id] = []  # Создаю "учётную запись" для заказов юзера
        await message.answer(text=f'{html.bold(html.quote(user_name))}, '
                                  f'Hallo !\nI am MINI APP Bot'
                                  f'I have been already started <b>{insgesamt}</b> by users, like you 🎲',
                             parse_mode=ParseMode.HTML)
        await message.answer("Put on the Pizza Button please to open Web App ↙️",
                             reply_markup=show_my_orders_kb)
    else:
        print('start else works')
        await insert_new_user_in_table(user_id, user_name)
        server_cart[user_id] = []
        insgesamt = await get_user_count()
        await message.answer(text=f'Bot was restated on server\n\n'
                                        f'Total users: <b>{insgesamt}</b>\n\n🔥')
        await message.delete()


@ch_router.message(Command('help'))
async def help_command(message: Message):
    user_id = str(message.from_user.id)
    temp_data = users_db[user_id]['bot_answer']
    if temp_data:
        with suppress(TelegramBadRequest):
            await temp_data.delete()
            users_db[user_id]['bot_answer'] = ''
    att = await message.answer(help_answer)
    # await message.answer(help_answer)
    users_db[user_id]['bot_answer'] = att
    await asyncio.sleep(2)
    await message.delete()


@ch_router.message(SHOW_BUTTON())
async def show_my_orders_command(message: Message):
    user_id = message.from_user.id
    ans_msg = await return_orders(user_id)
    await message.answer(ans_msg)
    await asyncio.sleep(2)
    await message.delete()

@ch_router.message(Command('my_orders'))
async def show_my_orders_command_slash(message: Message):
    user_id = message.from_user.id
    ans_msg = await return_orders(user_id)
    await message.answer(ans_msg)
    await asyncio.sleep(2)
    await message.delete()


@ch_router.message(Command('about_project'))
async def about_project_command(message: Message):
    await message.answer(about_project)
    await asyncio.sleep(2)
    await message.delete()


@ch_router.message(Command('admin'), IS_ADMIN())
async def send_message(message: Message, state: FSMContext):

    await message.answer(admin_eintritt)



@ch_router.message(Command('send_msg'), IS_ADMIN())
async def send_message(message: Message, state: FSMContext):
    await state.set_state(FSM_ST.admin)
    await message.answer('Schreib ihre Nachrichten')


@ch_router.message(Command('dump'), IS_ADMIN())
async def dump_db(message: Message, state: FSMContext):
    bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
    with open('save_db.json', 'w', encoding='utf-8') as file:
        json.dump(bot_dict, file, ensure_ascii=False, indent=4)

    await message.answer('Базы данных успешно записана !')


@ch_router.message(Command('load'), IS_ADMIN())
async def load_db(message: Message, state: FSMContext):
    with open('save_db.json', 'r') as file:
        recover_base = json.load(file)
        await dp.storage.set_data(key=bot_storage_key, data=recover_base)  # Обновляю словарь бота
        users_db.update(recover_base)
        # print('\n\n\n\n\n\nuser db = ',  users_db)
    await message.answer('Базы данных успешно загружены !')
    # await message.answer(users_db)


@ch_router.message(StateFilter(FSM_ST.admin))
async def send_message(message: Message, state: FSMContext):
    spisok_id = await return_tg_id()
    print('\n\n*******', spisok_id)
    counter = 0
    for chat_id in spisok_id:
        spam = message.text
        try:
            await message.bot.send_message(chat_id=chat_id[0], text=spam)
            counter += 1
        except TelegramForbiddenError:
            pass
        await asyncio.sleep(0.2)
    await state.set_state(FSM_ST.after_start)
    await message.answer(f'Mailing is done)))\n\nTotal mailing count: <b>{counter}</b>\n\n🔥')


@ch_router.message()
async def trasher(message: Message):
    print('TRASHER')
    await asyncio.sleep(1)
    await message.delete()