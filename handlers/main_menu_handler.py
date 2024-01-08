from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData

from keyboards import main_inline_kb, discount_decision

from bot import bot
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
        reply_markup=main_inline_kb.get_main_keyboard()
    )


@router.callback_query(F.data == "discount")
async def discount_handler(callback: CallbackData) -> None:

    about_discount_program = """
    Дорогой покупатель, рады сообщить вам о нашей дисконтной программе 💳!\n\nС каждой покупки вы получаете 5% бонусами,
которые можно использовать для оплаты до 50% от стоимости вашего следующего заказа 💰.\n
Это отличная возможность экономить на свежих цветах и создавать волшебные букеты 💐 с дополнительными преимуществами.\n
Хотите ли вы стать участником нашей дисконтной программы?
    """

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=about_discount_program,
        reply_markup=discount_decision.get_yes_no_keyboard()
    )
