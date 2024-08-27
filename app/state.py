from aiogram.fsm.state import StatesGroup, State


class UInfo(StatesGroup):
    service = State()
    clientID = State()
    ClientSecrets = State()


class UserInfoForMake(StatesGroup):
    make_url = State()
    user_team_id = State()
    user_organisation_id = State()
    token = State()
