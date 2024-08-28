from aiogram.fsm.state import StatesGroup, State


class UInfo(StatesGroup):
    service = State()
    client_id = State()
    client_secrets = State()
    tg_bot_token = State()
    tg_chat_id = State()
    fb_inst_page_id = State()
    yt_channel_id = State()
    tt_account_id = State()
    gd_folder_id = State()


class UserInfoForMake(StatesGroup):
    make_url = State()
    user_team_id = State()
    user_organisation_id = State()
    token = State()
