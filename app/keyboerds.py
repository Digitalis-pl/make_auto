from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)


app_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='запостить контент', callback_data='push')],
    [KeyboardButton(text='показать аккаунты', callback_data='show_content'),
     KeyboardButton(text='изменить', callback_data='change')]
], resize_keyboard=True, input_field_placeholder='menu')

button_to_add_accs = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Введите список сервисов', callback_data='services_list')]
])

services_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='tiktok'), KeyboardButton(text='google-drive')],
    [KeyboardButton(text='instagram'),
     KeyboardButton(text='youtube')],
    [KeyboardButton(text='сохранить')]
], resize_keyboard=True, input_field_placeholder='menu')
