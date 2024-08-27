import os

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from .keyboerds import app_keyboard, button_to_add_accs, services_keyboard
from .state import UInfo
from data.services import Database
from .services import CreateConnections

from dotenv import load_dotenv

load_dotenv()

router = Router()

db = Database(os.getenv('SQLite_DB_NAME'))

service_urls = {'instagram': 'https://developers.facebook.com/', 'google-drive': 'https://console.cloud.google.com', 'youtube': 'https://console.cloud.google.com', 'tiktok': 'https://developers.tiktok.com/'}


@router.message(CommandStart())
async def cm_start(message: Message):
    await message.answer('Начало работы', reply_markup=app_keyboard)


@router.message(Command('help'))
async def cm_someinfo(message: Message):
    kb = keyboard.InlineKeyboardBuilder()
    el = [1, 2, 3, 4]
    for n in el:
        kb.add(keyboard.InlineKeyboardButton(text=str(n), callback_data=str(n)))
    await message.answer('чем могу помочь?', reply_markup=kb.as_markup())


@router.callback_query(F.data == 'services_list')
async def input_services(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('выберите сервисы', reply_markup=services_keyboard)
    await state.set_state(UInfo.service.state)


@router.message(UInfo.service)
async def input_services(message: Message, state: FSMContext):
    data = None
    if message.text == 'сохранить':
        await state.clear()
        await message.answer(f'ответ записан ваши аккаунты:', reply_markup=app_keyboard)
    elif message.text == 'instagram':
        await state.update_data(service=message.text)
        data = await state.get_data()
    elif message.text == 'google-drive':
        await state.update_data(service=message.text)
    elif message.text == 'youtube':
        await state.update_data(service=message.text)
        data = await state.get_data()
    elif message.text == 'tiktok':
        await state.update_data(service=message.text)
        data = await state.get_data()
    await message.answer(
        f'введите Client secret для {data['services']}\nИли создайте его в {service_urls[message.text]}')
    await state.set_state(UInfo.ClientSecrets.state)


@router.message(UInfo.ClientSecrets)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(ClientSecrets=message.text)
    await message.answer(f'введите Client ID')
    await state.set_state(UInfo.clientID.state)


@router.message(UInfo.clientID)
async def input_client_id(message: Message, state: FSMContext):
    await state.update_data(clientID=message.text)
    data = await state.get_data()
    data['user_id'] = message.from_user.id
    await db.insert_table(**data)
    await state.update_data(ClientSecrets=None)
    await message.answer(f'ответ записан, хотите добавить дополнительный сервис')
    await state.set_state(UInfo.service.state)


@router.message(F.photo)
async def photo_info(message: Message):
    await message.answer_photo(photo=message.photo[-1].file_id,
                               reply_markup=button_to_add_accs)


@router.callback_query(F.data == 'youtube')
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer('youtube')


@router.callback_query(F.data == 'tik/tok')
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer('tik/tok')


@router.callback_query(F.data == 'instagram')
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer('instagram')


@router.message(F.text == 'показать аккаунты')
async def show_settings(message: Message):
    data = await db.show_info(message.from_user.id)
    await message.answer(f'Ваши настройки:\n{data}')


@router.message(F.text == 'запостить')
async def push_content(message: Message):
    data = await db.show_info(message.from_user.id)
    await message.answer(f'Осталось отправить:\n{data}')
    await db.truncate_table(message.from_user.id)


@router.message(F.text == 'изменить')
async def push_content(message: Message, state: FSMContext):
    await db.truncate_table(message.from_user.id)
    await message.answer(f'Выберите сервисы ', reply_markup=services_keyboard)
    await state.set_state(UInfo.service.state)
