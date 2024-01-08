import asyncio
import os

from dotenv import load_dotenv

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

load_dotenv('.env')

API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    username = message.from_user.username

    await message.answer(text="Главное меню")

    await message.answer(
        text=f"Доброго времени суток <b>{username}</b> 👋!\n\nДобро пожаловать в бота Цветы Майя.\n\n"
        "Данный бот поможет вам выбрать лучший букет 💐, за сумму на которую вы рассчитываете.\n\n"    
        "Мы внимательно контролируем логистику и сроки доставки каждого букета 🧐. У нас "
        "работает команда профессиональных флористов, которые подберут и составят яркий "
        "букет на любой вкус и случай.\n\n"
        "Для нас дорог каждый клиент 🙏!"
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
