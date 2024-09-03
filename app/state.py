from aiogram.fsm.state import StatesGroup, State


class UInfo(StatesGroup):
    service = State()
    name = State()


class TelegramInfo(UInfo):
    tg_bot_token = State()
    tg_chat_id = State()


class MoreClientInfo(UInfo):
    client_id = State()
    client_secrets = State()


class YouTubeInfo(MoreClientInfo):
    yt_channel_id = State()


class FacebookInfo(MoreClientInfo):
    fb_page_id = State()


class InstagramInfo(MoreClientInfo):
    inst_page_id = State()


class TiktokInfo(MoreClientInfo):
    tt_account_id = State()


class GDInfo(MoreClientInfo):
    gd_folder_id = State()


class UserInfoForMake(StatesGroup):
    name = State()
    make_url = State()
    user_team_id = State()
    user_organisation_id = State()
    token = State()


class TemporaryData(StatesGroup):
    my_session_data = State()
    yes_no = State()


