import sqlite3


class Database:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    async def create_make_client_list(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS make_accs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            user_id INTEGER,
            make_url TEXT NOT NULL,
            team_id TEXT NOT NULL,
            organisation_id TEXT NOT NULL,
            token TEXT NOT NULL)""")

    async def create_make_client(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS make_one_acc (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            user_id INTEGER,
            make_url TEXT NOT NULL,
            team_id TEXT NOT NULL,
            organisation_id TEXT NOT NULL,
            token TEXT NOT NULL)""")

    async def create_yt_table(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS youtube (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            user_id INTEGER,
            yt_channel_id TEXT,
            client_id TEXT,
            client_secrets TEXT
            )""")

    async def create_tt_table(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS tiktok (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            user_id INTEGER,
            tt_account_id TEXT,
            client_id TEXT,
            client_secrets TEXT
            )""")

    async def create_tg_table(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS telegram (
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL UNIQUE,
               user_id INTEGER,
               tg_bot_token TEXT,
               tg_chat_id TEXT,
               client_id TEXT,
               client_secrets TEXT
               )""")

    async def create_ig_table(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS instagram (
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL UNIQUE,
               user_id INTEGER,
               fb_inst_page_id TEXT,
               client_id TEXT,
               client_secrets TEXT
               )""")

    async def create_fb_table(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS facebook (
                  id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL UNIQUE,
                  user_id INTEGER,
                  fb_inst_page_id TEXT,
                  client_id TEXT,
                  client_secrets TEXT
                  )""")

    async def create_gd_table(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS google_drive (
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL UNIQUE,
               user_id INTEGER,
               gd_folder_id TEXT,
               client_id TEXT,
               client_secrets TEXT
               )""")

    async def create_table_user(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS accs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            service TEXT NOT NULL,
            name TEXT,
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

    async def insert_table(self, user_id=None, service=None, name=None, client_id=None, client_secrets=None,
                           tg_bot_token=None, tg_chat_id=None, fb_inst_page_id=None,
                           yt_channel_id=None, tt_account_id=None, gd_folder_id=None):
        with self.connection:
            return self.cursor.execute(
                """INSERT INTO accs
                (user_id, service, name, client_id, client_secrets, gd_folder_id, user_id, tg_bot_token, 
                tg_chat_id, fb_inst_page_id, yt_channel_id, tt_account_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, service, name, client_id, client_secrets, gd_folder_id, user_id, tg_bot_token,
                 tg_chat_id, fb_inst_page_id, yt_channel_id, tt_account_id))

    async def insert_connection_table(self, service=None, client_id=None, user_id=None, client_secrets=None):
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO accs (user_id, service, client_id, client_secrets) VALUES (?, ?, ?, ?)',
                (user_id, service, client_id, client_secrets))

    async def insert_make_table(self, akk_name, user_id, make_url, user_team_id, user_organisation_id, token):
        with self.connection:
            return self.cursor.execute(
                """INSERT INTO make_accs (name, user_id, make_url, team_id, organisation_id, token)
                 VALUES (?, ?, ?, ?, ?, ?)""",
                (akk_name, user_id, make_url, user_team_id, user_organisation_id, token))

    async def insert_temporary_make_table(self, name, user_id, make_url, team_id, organisation_id, token):
        with self.connection:
            return self.cursor.execute(
                """INSERT INTO make_one_acc (name, user_id, make_url, team_id, organisation_id, token)
                 VALUES (?, ?, ?, ?, ?, ?)""",
                (name, user_id, make_url, team_id, organisation_id, token))

    async def insert_acc_table(self, data):
        with self.connection:
            keys = []
            service = data.pop('service')
            for el in data.keys():
                keys.append(el)
            return self.cursor.execute(f"""INSERT INTO {service} ({', '.join(keys)}) 
            VALUES ({', '.join(['?' for _ in keys])})""", (tuple(data.values())))

    #  async def insert_tt_table(self, user_id, tt_account_id, client_id, client_secrets, service):
    #      with self.connection:
    #          return self.cursor.execute(
    #              """INSERT INTO tt_accs (user_id, tt_account_id, client_id, client_secrets)
    #               VALUES (?, ?, ?, ?)""",
    #              (user_id, tt_account_id, client_id, client_secrets))

    #  async def insert_tg_table(self, user_id, tg_bot_token, tg_chat_id, service):
    #      with self.connection:
    #          return self.cursor.execute(
    #              """INSERT INTO tg_accs (user_id, tg_bot_token, tg_chat_id)
    #               VALUES (?, ?, ?)""",
    #              (user_id, tg_bot_token, tg_chat_id))

    #  async def insert_gd_table(self, user_id, gd_folder_id, client_id, client_secrets, service):
    #      with self.connection:
    #          return self.cursor.execute(
    #              """INSERT INTO gd_accs (user_id, gd_folder_id, client_id, client_secrets)
    #               VALUES (?, ?, ?, ?)""",
    #              (user_id, gd_folder_id, client_id, client_secrets))

    #  async def insert_fb_ig_table(self, user_id, fb_inst_page_id, client_id, client_secrets, service):
    #      with self.connection:
    #          return self.cursor.execute(
    #              """INSERT INTO fb_ig_accs (user_id, fb_inst_page_id, client_id, client_secrets)
    #               VALUES (?, ?, ?, ?)""",
    #              (user_id, fb_inst_page_id, client_id, client_secrets))

    async def show_make_info(self, user_id):
        with self.connection:
            self.cursor.execute("""SELECT name, make_url, team_id, organisation_id, token 
            FROM make_accs 
            WHERE user_id=?""", (user_id,))
            columns = [column[0] for column in self.cursor.description]
            values = self.cursor.fetchall()
            info = [dict(zip(columns, row)) for row in values]
            for el in info:
                for i in list(el.keys()):
                    if el[i] is None or i in ['id', 'user_id']:
                        del el[i]
            return info

    async def show_my_make_acc(self, user_id, name):
        with self.connection:
            self.cursor.execute("""SELECT user_id, name, make_url, team_id, organisation_id, token 
               FROM make_accs 
               WHERE user_id=? and name=?""", (user_id, name))
            columns = [column[0] for column in self.cursor.description]
            values = self.cursor.fetchall()
            info = [dict(zip(columns, row)) for row in values]
            for el in info:
                for i in list(el.keys()):
                    if el[i] is None or i in ['id', ]:
                        del el[i]
            return info

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

    async def show_acc(self, user_id, service):
        with self.connection:
            self.cursor.execute(f'SELECT * FROM {service} WHERE user_id=?', (user_id,))
            columns = [column[0] for column in self.cursor.description]
            values = self.cursor.fetchall()
            info = [dict(zip(columns, row)) for row in values]
            for el in info:
                for i in list(el.keys()):
                    if el[i] is None or i in ['id', 'user_id']:
                        del el[i]
            return info

    async def show_saved_acc(self, user_id, service, name):
        with self.connection:
            self.cursor.execute(f'SELECT * FROM {service} WHERE user_id=? and name=?', (user_id, name,))
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
            self.cursor.execute(f'DELETE FROM accs WHERE user_id=?', (user_id,))
            self.cursor.execute(f'DELETE FROM make_one_acc WHERE user_id=?', (user_id,))
