from aiogram.fsm.state import StatesGroup, State


class UInfo(StatesGroup):
    service = State()
    clientID = State()
    ClientSecrets = State()


