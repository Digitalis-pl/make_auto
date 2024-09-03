from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)


start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Make аккаунт')],
    [KeyboardButton(text='Загрузить контент')]], resize_keyboard=True, input_field_placeholder='menu')

yes_no_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Да')],
    [KeyboardButton(text='Нет')]], resize_keyboard=True, input_field_placeholder='menu')

app_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Make аккаунт')],
    [KeyboardButton(text='Готово')],
    [KeyboardButton(text='показать аккаунты'),
     KeyboardButton(text='изменить')]
], resize_keyboard=True, input_field_placeholder='menu')

create_connection_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать соединения')]
], resize_keyboard=True)

create_scenario_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать сценарий')]
], resize_keyboard=True)

push_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='выгрузить контент')]
], resize_keyboard=True)

make_acc = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Уже есть аккаунт')],
    [KeyboardButton(text='Заполнить новый аккаунт')]
], resize_keyboard=True, input_field_placeholder='menu')

button_to_add_accs = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Введите список сервисов', callback_data='services_list')]
])

services_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='tiktok'), KeyboardButton(text='google_drive'), KeyboardButton(text='instagram')],
    [KeyboardButton(text='youtube'), KeyboardButton(text='telegram')],
    [KeyboardButton(text='сохранить')]
], resize_keyboard=True, input_field_placeholder='menu')
