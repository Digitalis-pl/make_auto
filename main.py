import os
import asyncio
import logging

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from app.heandlers import router, db

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()


async def main():
    await db.create_table_user()
    await db.create_table_connections()
    await db.create_make_client_list()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
