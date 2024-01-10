"""
Модуль с main функции, которая запускает бота.


Автор: danisimore
Дата: 10.01.2024


В данном модуле подгружается .env файл, значение API токена из переменной окружения сохраняется в переменную Python.
Далее создается экземпляр класса бота и диспетчера. В диспетчере регистрируем роутер (он пока один), пропускаем
обновления и запускаем polling.
"""

import os
import asyncio

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
