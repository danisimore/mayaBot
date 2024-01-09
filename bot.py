import asyncio
import os

from dotenv import load_dotenv

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher

import handlers

load_dotenv('.env')

API_TOKEN = os.environ.get('API_TOKEN')
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)


async def main() -> None:
    """ Главная функция, которая запускает бота. """

    dp = Dispatcher()

    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
