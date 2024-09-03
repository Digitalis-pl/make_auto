from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext

from aiogram.types import Message

from main import db

from app.state import UInfo

#@router.callback_query(F.data == 'services_list')
#async def input_services(callback: CallbackQuery, state: FSMContext):
#    await callback.message.answer('выберите сервисы', reply_markup=services_keyboard)
#    await state.set_state(UInfo.service.state)


# @router.message(UInfo.name)
# async def nemed_acc(message: Message, state: FSMContext):
#    data = await state.get_data()
#    if data['service'] ==


# google_drive
#@router.message(UInfo.gd_folder_id)
#async def input_secrets(message: Message, state: FSMContext):
#    await state.update_data(gd_folder_id=message.text)
#    data = await state.get_data()
#    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
#    await state.set_state(UInfo.client_secrets.state)
#
#
## instagram, facebook
#@router.message(UInfo.fb_inst_page_id)
#async def input_secrets(message: Message, state: FSMContext):
#    await state.update_data(fb_inst_page_id=message.text)
#    data = await state.get_data()
#    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
#    await state.set_state(UInfo.client_secrets.state)
#
#
## youtube
#@router.message(UInfo.yt_channel_id)
#async def input_secrets(message: Message, state: FSMContext):
#    await state.update_data(yt_channel_id=message.text)
#    data = await state.get_data()
#    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
#    await state.set_state(UInfo.client_secrets.state)
#
#
## tiktok
#@router.message(UInfo.tt_account_id)
#async def input_secrets(message: Message, state: FSMContext):
#    await state.update_data(tt_account_id=message.text)
#    data = await state.get_data()
#    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
#    await state.set_state(UInfo.client_secrets.state)
#
#
## telegram
#@router.message(UInfo.tg_chat_id)
#async def input_secrets(message: Message, state: FSMContext):
#    await state.update_data(tg_chat_id=message.text)
#    await message.answer(f'Введите ваш bot token')
#    await state.set_state(UInfo.tg_bot_token.state)
#
#
#@router.message(UInfo.tg_bot_token)
#async def input_secrets(message: Message, state: FSMContext):
#    await state.update_data(tg_bot_token=message.text)
#    data = await state.get_data()
#    data['user_id'] = message.from_user.id
#    await db.insert_table(**data)
#    await db.insert_tg_table(**data)
#    await state.set_data({})
#    await message.answer(f'ответ записан, хотите добавить дополнительный сервис')
#    await state.set_state(UInfo.service.state)
#
#
## Дальше общие шаги для получения client_secrets и client_id
#@router.message(UInfo.client_secrets)
#async def input_secrets(message: Message, state: FSMContext):
#    await state.update_data(client_secrets=message.text)
#    await message.answer(f'введите Client ID')
#    await state.set_state(UInfo.client_id.state)
#
#
#@router.message(UInfo.client_id)
#async def input_client_id(message: Message, state: FSMContext):
#    await state.update_data(client_id=message.text)
#    data = await state.get_data()
#    data['user_id'] = message.from_user.id
#    await db.insert_table(**data)
#    if data['service'] == 'google_drive':
#        await db.insert_gd_table(**data)
#    if data['service'] in 'youtube':
#        await db.insert_yt_table(**data)
#    if data['service'] in ['facebook', 'instagram']:
#        await db.insert_fb_ig_table(**data)
#    if data['service'] == 'tiktok':
#        await db.insert_tt_table(**data)
#    await state.set_data({})
#    await message.answer(f'ответ записан, хотите добавить дополнительный сервис')
#    await state.set_state(UInfo.service.state)
#