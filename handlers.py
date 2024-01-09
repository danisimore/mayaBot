import bot_message_texts

from aiogram import Router, F, types

from aiogram.types import FSInputFile

from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from bot import bot
from states.discount_registration import DiscountRegistration

from keyboards.inline_keyboard_builder import get_inline_keyboard

router = Router()

main_inline_keyboard_structure = {
    "Хочу скидку! 💸": "discount",
    "Посмотреть ассортимент": "test2",
}


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
        reply_markup=get_inline_keyboard(main_inline_keyboard_structure),
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

    # Словарь содержащий данные ТЕКСТ_КНОПКИ : CALLBACK_DATA
    keyboard_structure = {
        "ДА!": "discount_yes",
        "Пожалуй позже": "cancel",
    }

    # Загружаем изображение
    image = FSInputFile("images/discount.jpg")

    await bot.send_photo(
        chat_id=user_id,
        photo=image,
        caption=bot_message_texts.ABOUT_DISCOUNT_PROGRAM,
        reply_markup=get_inline_keyboard(keyboard_structure),
    )

    # Устанавливаем состояние конечного автомата.
    await state.set_state(DiscountRegistration.making_decision)


@router.callback_query(F.data == "cancel")
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
        reply_markup=get_inline_keyboard(main_inline_keyboard_structure)
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

    # Словарь содержащий данные ТЕКСТ_КНОПКИ : CALLBACK_DATA
    keyboard_structure = {
        "Отменить и вернуться в главное меню": "cancel",
    }

    await bot.send_message(
        chat_id=user_id,
        text="Отлично, теперь мне необходимо узнать ваше имя.\nПожалуйста, напишите мне свое имя)\n\n"
             "<b>Внимание, указывайте свое настоящее имя, иначе заявка будет отклонена оператором!</b>\n\n",
        reply_markup=get_inline_keyboard(keyboard_structure),
    )

    await state.set_state(DiscountRegistration.entering_name)


@router.message(DiscountRegistration.entering_name)
async def discount_entered_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Handler для обработки сообщения с именем пользователя.

    Ветка:
    '/start' -> 'Хочу скидку! 💸' -> 'ДА!' -> Ввод имени

    ---

    :param message: сообщение с именем пользователя
    :param state: Состояние конечного автомата
    :return:
    """

    # Словарь содержащий данные ТЕКСТ_КНОПКИ : CALLBACK_DATA
    keyboard_structure = {
        "Изменить имя": "change_entered_name",
        "Отменить и вернуться в главное меню": "cancel",
    }

    await state.update_data(user_entered_name=message.text)

    await message.answer(
        text="Отлично, теперь введите вашу фамилию",
        reply_markup=get_inline_keyboard(keyboard_structure, 1, 1),
    )
