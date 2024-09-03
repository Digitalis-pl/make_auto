from app.heandler_dir import router, Message, F, create_scenario_keyboard, create_connection_keyboard


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