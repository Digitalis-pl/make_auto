import sqlite3


class Database:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    async def create_table_user(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS accs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            service TEXT NOT NULL,
            clientID TEXT NOT NULL,
            ClientSecrets TEXT)""")

    async def create_table_connections(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY,
            connection_id INTEGER,
            name TEXT NOT NULL,
            accountName TEXT NOT NULL,
            accountLabel TEXT NOT NULL)
            """)

    async def insert_table(self, service=None, clientID=None, user_id=None, ClientSecrets=None):
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO accs (user_id, service, clientID, ClientSecrets) VALUES (?, ?, ?, ?)',
                (user_id, service, clientID, ClientSecrets))

    async def show_info(self, user_id):
        with self.connection:
            self.cursor.execute(f'SELECT service, clientID, secrets FROM accs WHERE user_id=?', (user_id,))
            return self.cursor.fetchall()

    async def truncate_table(self, user_id):
        with self.connection:
            return self.cursor.execute(f'DELETE FROM accs WHERE user_id=?', (user_id,))
