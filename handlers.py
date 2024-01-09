from aiogram import Router, F, types

from aiogram.types import FSInputFile

from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from bot import bot
from keyboards import main_inline_kb, discount_decision, cancel_inline_kb
from states.discount_registration import DiscountRegistration
import bot_message_texts

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """
    Функция для обработки команды /start.

    Ветка:
    '/start'

    ---

    :param message: Сообщение, полученное от пользователя
    :param state: Состояние конечного автомата
    :return:
    """

    # Получаем имя пользователя
    first_name = message.from_user.first_name

    # Устанавливаем состояние конечного автомата в None, т.к. оно может быть и не None.
    await state.set_state(None)

    await message.answer(text=bot_message_texts.MAIN_MENU)

    await message.answer(
        text=bot_message_texts.MAIN_MENU_TEXT % first_name,
        reply_markup=main_inline_kb.get_main_keyboard()
    )


@router.callback_query(StateFilter(None), F.data == "discount")
async def discount_handler(callback: CallbackData, state: FSMContext) -> None:
    """
    Handler для обработки события нажатия кнопки 'Хочу скидку! 💸'.

    Ветка:
    '/start' -> 'Хочу скидку! 💸'

    ---

    :param callback: Callback, полученный после нажатия пользователем inline кнопки
    :param state: Состояние конечного автомата
    :return:
    """

    user_id = callback.from_user.id

    # Загружаем изображение
    image = FSInputFile("images/discount.jpg")

    await bot.send_photo(
        chat_id=user_id,
        photo=image,
        caption=bot_message_texts.ABOUT_DISCOUNT_PROGRAM,
        reply_markup=discount_decision.get_yes_no_keyboard(),
    )

    # Устанавливаем состояние конечного автомата.
    await state.set_state(DiscountRegistration.making_decision)


@router.callback_query(DiscountRegistration.making_decision, F.data == "cancel")
async def discount_later_handler(callback: CallbackData, state: FSMContext) -> None:
    """
    Handler для обработки события нажатия кнопки 'Пожалуй позже'.

    Ветка:
    '/start' -> 'Хочу скидку! 💸' -> 'Пожалуй позже'

    ---

    :param callback: Callback, полученный после нажатия пользователем inline кнопки
    :param state: Состояние конечного автомата
    :return:
    """

    user_id = callback.from_user.id
    first_name = callback.from_user.first_name

    await bot.send_message(
        chat_id=user_id,
        text=bot_message_texts.MAIN_MENU,
    )

    await bot.send_message(
        chat_id=user_id,
        text=bot_message_texts.MAIN_MENU_TEXT % first_name,
        reply_markup=main_inline_kb.get_main_keyboard()
    )

    # Так как пользователь отказывается от оформления дисконта, устанавливаем состояние None.
    await state.set_state(None)


@router.callback_query(DiscountRegistration.making_decision, F.data == "discount_yes")
async def discount_yes_handler(callback: CallbackData, state: FSMContext) -> None:
    """
    Handler для обработки события нажатия кнопки 'ДА!'.

    Ветка:
    '/start' -> 'Хочу скидку! 💸' -> 'ДА!'

    ---

    :param callback: Callback, полученный после нажатия пользователем inline кнопки
    :param state: Состояние конечного автомата
    :return:
    """

    user_id = callback.from_user.id

    await bot.send_message(
        chat_id=user_id,
        text="Отлично, теперь мне необходимо узнать ваше имя.\nПожалуйста, напишите мне свое имя)\n\n"
             "<b>Внимание, указывайте свое настоящее имя, иначе заявка будет отклонена оператором!</b>\n\n",
        reply_markup=cancel_inline_kb.get_cancel_keyboard(),
    )

    await state.set_state(DiscountRegistration.entering_name)
