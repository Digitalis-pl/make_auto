import sqlite3


class Database:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    async def create_make_client_list(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS make_accs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            make_url TEXT NOT NULL,
            team_id TEXT NOT NULL,
            organisation_id TEXT NOT NULL,
            token TEXT NOT NULL)""")

    async def create_table_user(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS accs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            service TEXT NOT NULL,
            client_id TEXT,
            client_secrets TEXT,
            gd_folder_id TEXT,
            tg_bot_token TEXT,
            tg_chat_id TEXT,
            fb_inst_page_id TEXT,
            yt_channel_id TEXT,
            tt_account_id TEXT)""")

    async def create_table_connections(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY,
            connection_id INTEGER,
            name TEXT NOT NULL,
            accountName TEXT NOT NULL,
            accountLabel TEXT NOT NULL)
            """)

    async def insert_table(self, user_id=None, service=None, client_id=None, client_secrets=None,
                           tg_bot_token=None, tg_chat_id=None, fb_inst_page_id=None,
                           yt_channel_id=None, tt_account_id=None, gd_folder_id=None):
        with self.connection:
            return self.cursor.execute(
                """INSERT INTO accs
                (user_id, service, client_id, client_secrets, gd_folder_id, user_id, tg_bot_token, 
                tg_chat_id, fb_inst_page_id, yt_channel_id, tt_account_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, service, client_id, client_secrets, gd_folder_id, user_id, tg_bot_token,
                 tg_chat_id, fb_inst_page_id, yt_channel_id, tt_account_id))

    async def insert_connection_table(self, service=None, client_id=None, user_id=None, client_secrets=None):
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO accs (user_id, service, client_id, client_secrets) VALUES (?, ?, ?, ?)',
                (user_id, service, client_id, client_secrets))

    async def insert_make_table(self, user_id, make_url, user_team_id, user_organisation_id, token):
        with self.connection:
            return self.cursor.execute(
                """INSERT INTO make_accs (user_id, make_url, team_id, organisation_id, token)
                 VALUES (?, ?, ?, ?, ?)""",
                (user_id, make_url, user_team_id, user_organisation_id, token))

    async def show_make_info(self, user_id):
        with self.connection:
            self.cursor.execute("""SELECT make_url, team_id, organisation_id, token 
            FROM make_accs 
            WHERE user_id=?""", (user_id,))
            return self.cursor.fetchall()

    async def show_info(self, user_id):
        with self.connection:
            self.cursor.execute(f'SELECT * FROM accs WHERE user_id=?', (user_id,))
            columns = [column[0] for column in self.cursor.description]
            values = self.cursor.fetchall()
            info = [dict(zip(columns, row)) for row in values]
            for el in info:
                for i in list(el.keys()):
                    if el[i] is None or i in ['id', 'user_id']:
                        del el[i]
            return info

    async def truncate_table(self, user_id):
        with self.connection:
            return self.cursor.execute(f'DELETE FROM accs WHERE user_id=?', (user_id,))
