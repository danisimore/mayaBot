from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData

from keyboards.main_keyboard import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """
    Функция для обработки команды /start.

    :param message: Сообщение, полученное от пользователя
    :return:
    """
    username = message.from_user.username

    await message.answer(text="Главное меню")

    await message.answer(
        text=f"Доброго времени суток <b>{username}</b> 👋!\n\nДобро пожаловать в бота Цветы Майя.\n\n"
             "Данный бот поможет вам выбрать лучший букет 💐, за сумму на которую вы рассчитываете.\n\n"
             "Мы внимательно контролируем логистику и сроки доставки каждого букета 🧐. У нас "
             "работает команда профессиональных флористов, которые подберут и составят яркий "
             "букет на любой вкус и случай.\n\n"
             "Для нас дорог каждый клиент 🙏!",
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data == "discount")
async def discount_handler(callback: CallbackData) -> None:
    print("triggered!")
