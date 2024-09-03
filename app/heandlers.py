import os

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import keyboard
from aiogram.fsm.context import FSMContext


from .keyboerds import (app_keyboard, button_to_add_accs, services_keyboard,
                        create_connection_keyboard, create_scenario_keyboard,
                        push_button, make_acc, start_keyboard)
from .state import UInfo, UserInfoForMake, TemporaryData, TelegramInfo, YouTubeInfo, FacebookInfo, InstagramInfo, \
    TiktokInfo, GDInfo, MoreClientInfo
from data.services import Database

from dotenv import load_dotenv

load_dotenv()

router = Router()

db = Database(os.getenv('SQLite_DB_NAME'))

service_urls = {'instagram': 'https://developers.facebook.com/', 'google_drive': 'https://console.cloud.google.com',
                'youtube': 'https://console.cloud.google.com', 'tiktok': 'https://developers.tiktok.com/'}


def create_keyboard(el_list):
    builder = keyboard.ReplyKeyboardBuilder()
    for el in el_list:
        builder.add(keyboard.KeyboardButton(text=el['name']))
    return builder


async def already_have_acc(message: Message, state: FSMContext):
    acc_list = await db.show_acc(message.from_user.id, message.text)
    print(acc_list)
    if len(acc_list) > 0:
        kb = create_keyboard(acc_list)
        return await message.answer('у вас есть сохраненные аккаунты, хотите использовать их или записать новый?',
                                    reply_markup=kb.as_markup(resize_keyboard=True))
    else:
        await state.update_data(service=message.text)
        await state.set_state(UInfo.name)
        return await message.answer('Придумайте название для странички или введите название канала')


class ServiceCommand:
    def __init__(self, service, message: Message, state: FSMContext):
        self.state = state
        self.service = service
        self.message = message

    async def next_state(self):
        await already_have_acc(self.message, self.state)

    async def process_info(self):
        service_mapping = {
            'telegram': TelegramInfo.tg_chat_id,
            'youtube': YouTubeInfo.yt_channel_id,
            'facebook': FacebookInfo.fb_page_id,
            'instagram': InstagramInfo.inst_page_id,
            'tiktok': TiktokInfo.tt_account_id,
            'google_drive': GDInfo.gd_folder_id
        }

        next_state = service_mapping.get(self.service)

        return [self.service, next_state]


# стартовая команда


@router.message(CommandStart())
async def cm_start(message: Message):
    await db.truncate_table(message.from_user.id)
    await message.answer('Для работы вам необходим аккаунт в https://www.make.com', reply_markup=make_acc)


# Блок для заполнения информации об аккаунте make
@router.message(F.text == 'Заполнить новый аккаунт')
async def write_make_name(message: Message, state: FSMContext):
    await state.set_state(UserInfoForMake.name.state)
    await message.answer(
        """ведите имя для вашего аккаунта)""",
        reply_markup=ReplyKeyboardRemove())


@router.message(UserInfoForMake.name)
async def take_make_info(message: Message, state: FSMContext):
    await state.set_state(UserInfoForMake.make_url.state)
    await state.update_data(akk_name=message.text)
    await message.answer(
        """ведите url для соединения с вашим аккаунтом вы можете скопировать его в адресной строке
         (пример:https://eu2.make.com/... необходима только эта часть)""",
        reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'Уже есть аккаунт')
async def choose_make_info(message: Message, state: FSMContext):
    acs_list = await db.show_make_info(message.from_user.id)
    await state.set_state(TemporaryData.my_session_data.state)
    kb = create_keyboard(acs_list)
    await message.answer(
        """Выберите аккаунт""",
        reply_markup=kb.as_markup(resize_keyboard=True))


@router.message(TemporaryData.my_session_data)
async def get_acc_info(message: Message, state: FSMContext):
    my_acc = await db.show_my_make_acc(message.from_user.id, message.text)
    print(my_acc)
    await db.insert_temporary_make_table(**my_acc[0])
    await state.clear()
    await message.answer('Вы можете посмотреть всю информацию при нажатии кнопки Make аккаунт',
                         reply_markup=start_keyboard)


@router.message(UserInfoForMake.make_url)
async def write_make_url(message: Message, state: FSMContext):
    await state.update_data(make_url=message.text)
    await state.set_state(UserInfoForMake.user_team_id.state)
    await message.answer('Введите teamId')


@router.message(UserInfoForMake.user_team_id)
async def write_make_team_id(message: Message, state: FSMContext):
    await state.update_data(user_team_id=message.text)
    await state.set_state(UserInfoForMake.user_organisation_id.state)
    await message.answer('Введите user_organisation_id')


@router.message(UserInfoForMake.user_organisation_id)
async def write_make_organisation_id(message: Message, state: FSMContext):
    await state.update_data(user_organisation_id=message.text)
    await state.set_state(UserInfoForMake.token.state)
    await message.answer('Введите api token')


@router.message(UserInfoForMake.token)
async def write_make_token(message: Message, state: FSMContext):
    await state.update_data(token=message.text)
    data = await state.get_data()
    data['user_id'] = message.from_user.id
    await db.insert_make_table(**data)
    await state.clear()
    await message.answer(
        'Данные аккаунта записаны, вы можете посмотреть всю информацию при нажатии кнопки Make аккаунт',
        reply_markup=start_keyboard)


@router.message(F.text == 'Make аккаунт')
async def show_make_settings(message: Message):
    data = await db.show_make_info(message.from_user.id)
    await message.answer(f'Ваши настройки:\n{data}')


# Начало работы с контентом


@router.message(F.text == 'Загрузить контент')
async def start_work_with_content(message: Message):
    await message.answer('Загрузите фотографию', reply_markup=ReplyKeyboardRemove())


# Выбор и заполнение данных об аккаунтах пользователя


@router.callback_query(F.data == 'services_list')
async def input_services(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('выберите сервисы', reply_markup=services_keyboard)
    await state.set_state(UInfo.service.state)


@router.message(UInfo.service)
async def input_services(message: Message, state: FSMContext):
    if message.text == 'сохранить':
        await state.clear()
        await message.answer(f'Ответ записан ваши аккаунты:', reply_markup=app_keyboard)
    else:
        service = ServiceCommand(message.text, message, state)
        await service.next_state()


@router.message(UInfo.name)
async def nemed_acc(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    service = ServiceCommand(data['service'], message, state)
    step = await service.process_info()
    await state.set_state(step[1])
    await message.answer('Введите id папки, странички, канала или чата')


# google_drive
@router.message(GDInfo.gd_folder_id)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(gd_folder_id=message.text)
    data = await state.get_data()
    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
    await state.set_state(GDInfo.client_secrets.state)


# instagram, facebook
@router.message(InstagramInfo.inst_page_id)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(fb_inst_page_id=message.text)
    data = await state.get_data()
    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
    await state.set_state(InstagramInfo.client_secrets.state)


# youtube
@router.message(YouTubeInfo.yt_channel_id)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(yt_channel_id=message.text)
    data = await state.get_data()
    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
    await state.set_state(YouTubeInfo.client_secrets.state)


# tiktok
@router.message(TiktokInfo.tt_account_id)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(tt_account_id=message.text)
    data = await state.get_data()
    await message.answer(f'Введите Client secret {data['service']}\nИли создайте его в {service_urls[data['service']]}')
    await state.set_state(TiktokInfo.client_secrets.state)


# telegram
@router.message(TelegramInfo.tg_chat_id)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(tg_chat_id=message.text)
    await message.answer(f'Введите ваш bot token')
    await state.set_state(TelegramInfo.tg_bot_token.state)


@router.message(TelegramInfo.tg_bot_token)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(tg_bot_token=message.text)
    data = await state.get_data()
    data['user_id'] = message.from_user.id
    del data['name']
    await db.insert_table(**data)
    #await db.in(**data)
    await state.set_data({})
    await message.answer(f'ответ записан, хотите добавить дополнительный сервис')
    await state.set_state(UInfo.service.state)


# Дальше общие шаги для получения client_secrets и client_id
@router.message(MoreClientInfo.client_secrets)
async def input_secrets(message: Message, state: FSMContext):
    await state.update_data(client_secrets=message.text)
    await message.answer(f'введите Client ID')
    await state.set_state(MoreClientInfo.client_id.state)


@router.message(MoreClientInfo.client_id)
async def input_client_id(message: Message, state: FSMContext):
    await state.update_data(client_id=message.text)
    data = await state.get_data()
    data['user_id'] = message.from_user.id
    #await db.insert_acc_table(**data)
    await db.insert_acc_table(data)
    await state.set_data({})
    await message.answer(f'ответ записан, хотите добавить дополнительный сервис')
    await state.set_state(UInfo.service.state)


# часть которая как будто создает контент


@router.message(F.photo)
async def photo_info(message: Message):
    await message.answer_photo(photo=message.photo[-1].file_id,
                               reply_markup=button_to_add_accs)


# Блок для проверки и изменения введенных данных


@router.message(F.text == 'показать аккаунты')
async def show_settings(message: Message):
    data = await db.show_info(message.from_user.id)
    await message.answer(f'Ваши настройки:\n{data}')


@router.message(F.text == 'изменить')
async def push_content(message: Message, state: FSMContext):
    await db.truncate_table(message.from_user.id)
    await message.answer(f'Выберите сервисы ', reply_markup=services_keyboard)
    await state.set_state(UInfo.service.state)


# Блок для взаимодействия с make api


@router.message(F.text == 'Готово')
async def push_content(message: Message):
    """Будет отправлять данные и контент боту публикатору"""
    await message.answer(f'Данные записаны, теперь создадим соединения',
                         reply_markup=create_connection_keyboard)


@router.message(F.text == 'Создать соединения')
async def push_content(message: Message):
    """Будет отправлять запрос на создание соединений и записывать х в базу соединений"""
    data = {}
    await message.answer(f'Соединения успешно созданы\nваш список id:{data}\nСоздайте сценарий',
                         reply_markup=create_scenario_keyboard)


@router.message(F.text == 'Создать сценарий')
async def push_content(message: Message):
    """Будет формировать чертеж и отправлять запрос на создание сценария"""
    await message.answer(f'Сценарий создан, можно загружать контент',
                         reply_markup=push_button)


@router.message(F.text == 'выгрузить контент')
async def push_content(message: Message):
    """Будет отправлять запрос на запуск сценария и отправлять данные и контент боту публикатору"""
    await message.answer(f'Данные отправлены, список сервисов отчищен, вы можете создать новый контент')
    await db.truncate_table(message.from_user.id)
    await message.answer('Загрузите фотографию', reply_markup=ReplyKeyboardRemove())
