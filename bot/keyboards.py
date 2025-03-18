from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

my_orders_button = KeyboardButton(text='* Show my Orders *')

show_my_orders_kb = ReplyKeyboardMarkup(
    keyboard=[[my_orders_button]],
    resize_keyboard=True)