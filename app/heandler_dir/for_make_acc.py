# стартовая команда
from app.heandler_dir import router, CommandStart, Message, db, F, FSMContext, make_acc, ReplyKeyboardRemove, \
    create_keyboard,start_keyboard

from app.state import UserInfoForMake, TemporaryData


@router.message(CommandStart())
async def cm_start(message: Message):
    await db.truncate_table(message.from_user.id)
    await message.answer('Для работы вам необходим аккаунт в https://www.make.com', reply_markup=make_acc)


# Блок для заполнения информации об аккаунте make
@router.message(F.text == 'Заполнить новый аккаунт')
async def write_make_name(message: Message, state: FSMContext):
    await state.set_state(UserInfoForMake.akk_name.state)
    await message.answer(
        """ведите имя для вашего аккаунта)""",
        reply_markup=ReplyKeyboardRemove())


@router.message(UserInfoForMake.akk_name)
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
