"""
Модуль с хэндлерами, которые обрабатывают различные события.


Автор: danisimore
Дата: 10.01.2024


• cmd_start - обработка команды start, если id пользователя, совпадает с MANAGER_CHAT_ID из .env файла, то
              отправляется сообщение "Активирован режим администратора!" и далее ничего не происходит, т.к.
              этот режим подразумевает ожидание сообщений от бота с данными о пользователе, который прошел
              регистрацию в дисконтной программе. Иначе отправляет сообщение с главным меню;

• discount_handler - обрабатывает нажатие кнопки 'Хочу скидку! 💸'. Устанавливает состояние конечного автомата
                     в making_decision. На этом этапе бот информирует пользователя о дисконтной программе
                     и предлагает в ней зарегистрироваться либо вернуться в главное меню;

• discount_later_handler - Handler для обработки события нажатия кнопки 'Пожалуй позже'. Сценарий, если пользователь
                           отказался от регистрации в дисконтной программе. Возвращает пользователя в
                           главное меню путем вызова функции show_main_menu_from_callback из модуля show_main_menu;

• discount_yes_handler - Handler для обработки события нажатия кнопки 'ДА!'. Сценарий, если пользователь согласился
                         на регистрацию в дисконтной программе. Проверяет зарегистрирован ли пользователь в дисконтной
                         программе путем вызова функции select_user_data. Если она возвращает False, то процесс
                         регистрации продолжается и бот запрашивает у пользователя имя, устанавливая состояние конечного
                         автомата в entering_name. Если select_user_data возвращает True, то пользователю отправляется
                         сообщение с главным меню, путем вызова функции show_main_menu_from_callback.

• discount_entered_name_handler - Handler для обработки введенного пользователем имени, срабатывает только если
                                  состояние конечного автомата entering_name. Сохраняет в state введенное имя и
                                  устанавливает FSM в entering_last_name.

• discount_entered_last_name_handler - Handler для обработки введенной пользователем фамилии, срабатывает только если
                                       FSM entering_last_name. Сохраняет в state введенную фамилию и устанавливает
                                       FSM в entering_patronymic.

• discount_no_patronymic_handler - Handler для обработки сценария, если у пользователя нет отчества. В state
                                   сохраняет значение "Отчество отсутствует" и переводит пользователя на следующий
                                   шаг - ввод номера телефона, устанавливая при этом FSM entering_phone_number.

• discount_entered_patronymic_handler - Handler для обработки введенного пользователем отчества, срабатывает только если
                                        FSM entering_patronymic. Также переводит пользователя на шаг ввода номера
                                        телефона, устанавливая FSM entering_phone_number.

• discount_entered_phone_number_handler - Handler для обработки введенного пользователем номера телефона, а также
                                          проверки корректности введенных им данных. Срабатывает только если FSM
                                          entering_phone_number. Просит ввести номер телефона еще раз,
                                          если он не прошел валидацию. Далее выводит пользователю всю введенную им
                                          информацию и устанавливает FSM в checking_entered_data, предлагая пользователю
                                          подтвердить корректность введенных данных или заполнить все снова.

• discount_data_is_correct_handler - Handler для обработки сценария, если пользователь подтвердил, что данные корректны.
                                     Сбрасывает состояния и вносит его username и номер телефона в БД, отправляя при
                                     этом все данные менеджеру, id которого указан в переменной окружения
                                     MANAGER_CHAT_ID.
"""

import os

import bot_message_texts

from aiogram import Router, F, types

from aiogram.types import FSInputFile

from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv

from main import bot
from states.discount_registration import DiscountRegistration

from keyboards.inline_keyboard_builder import get_inline_keyboard

from services.phone_number_validator import phone_num_validator
from services.generate_user_data import generate_user_data
from services.show_main_menu import show_main_menu_from_callback

from database.insert_user_data import insert_user_data
from database.select_user_data import select_user_data

load_dotenv('.env')

router = Router()

MANAGER_CHAT_ID = os.environ.get('MANAGER_CHAT_ID')

MAIN_INLINE_KEYBOARD_STRUCTURE = {
    "Хочу скидку! 💸": "discount",
    "Посмотреть ассортимент": "test2",
}

DEFAULT_DISCOUNT_REGISTRATION_KEYBOARD_STRUCTURE = {
    "Начать сначала": "discount_yes",
    "Отменить и вернуться в главное меню": "cancel",
}


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """
    Функция для обработки команды /start.

    ---
    /start
    ---

    :param message: Сообщение, полученное от пользователя
    :param state: Состояние конечного автомата
    :return:
    """

    if message.from_user.id == int(MANAGER_CHAT_ID):
        await bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text="Активирован режим администратора!"
        )
    else:
        # Получаем имя пользователя
        first_name = message.from_user.first_name

        # Устанавливаем состояние конечного автомата в None, т.к. оно может быть и не None.
        await state.set_state(None)

        await message.answer(text=bot_message_texts.MAIN_MENU)

        await message.answer(
            text=bot_message_texts.MAIN_MENU_TEXT % first_name,
            reply_markup=get_inline_keyboard(MAIN_INLINE_KEYBOARD_STRUCTURE),
        )


@router.callback_query(StateFilter(None), F.data == "discount")
async def discount_handler(callback: CallbackData, state: FSMContext) -> None:
    """
    Handler для обработки события нажатия кнопки 'Хочу скидку! 💸'.

    ---
    /start -> Хочу скидку! 💸
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

    ---
    /start -> Хочу скидку! 💸 -> Пожалуй позже
    ---

    :param callback: Callback, полученный после нажатия пользователем inline кнопки
    :param state: Состояние конечного автомата
    :return:
    """

    inline_keyboard = get_inline_keyboard(MAIN_INLINE_KEYBOARD_STRUCTURE)

    await show_main_menu_from_callback(
        callback=callback,
        bot=bot,
        inline_keyboard=inline_keyboard,
        state=state
    )


@router.callback_query(F.data == "discount_yes")
async def discount_yes_handler(callback: CallbackData, state: FSMContext) -> None:
    """
    Handler для обработки события нажатия кнопки 'ДА!'.

    ---
    Ветка:
    /start -> Хочу скидку! 💸 -> ДА! -> Ввод имени
    ---


    :param callback: Callback, полученный после нажатия пользователем inline кнопки
    :param state: Состояние конечного автомата
    :return:
    """

    user_id = callback.from_user.id
    username = callback.from_user.username

    is_registered = select_user_data(username)

    if not is_registered:
        # Словарь содержащий данные ТЕКСТ_КНОПКИ : CALLBACK_DATA
        keyboard_structure = {
            "Отменить и вернуться в главное меню": "cancel",
        }

        await bot.send_message(
            chat_id=user_id,
            text="Отлично, теперь мне необходимо узнать ваше имя.\nПожалуйста, напишите мне свое имя)\n\n"
                 "<b>Внимание, указывайте свое настоящее имя, иначе заявка будет отклонена оператором!</b>",
            reply_markup=get_inline_keyboard(keyboard_structure),
        )

        await state.set_state(DiscountRegistration.entering_name)
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Вы уже зарегистрированы в дисконтной программе!\n\n"
                 "Спасибо за то, что выбрали нас ❤",
        )

        inline_keyboard = get_inline_keyboard(MAIN_INLINE_KEYBOARD_STRUCTURE)

        await show_main_menu_from_callback(
            callback=callback,
            bot=bot,
            inline_keyboard=inline_keyboard,
            state=state
        )


@router.message(DiscountRegistration.entering_name)
async def discount_entered_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Handler для обработки сообщения с именем пользователя.

    ---
    /start -> Хочу скидку! 💸 -> ДА! -> Ввод имени -> Ввод фамилии
    ---

    :param message: сообщение с именем пользователя;
    :param state: Состояние конечного автомата;
    :return:
    """

    await state.update_data(user_entered_name=message.text)

    await message.answer(
        text="Отлично, теперь введите вашу фамилию\n\n"
             "<b>Внимание, указывайте свое настоящую фамилию, иначе заявка будет отклонена оператором!</b>",
        reply_markup=get_inline_keyboard(DEFAULT_DISCOUNT_REGISTRATION_KEYBOARD_STRUCTURE, 1, 1),
    )

    await state.set_state(DiscountRegistration.entering_last_name)


@router.message(DiscountRegistration.entering_last_name)
async def discount_entered_last_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Handler для обработки сообщения с фамилией пользователя.

    ---
    /start -> Хочу скидку! 💸 -> ДА! -> Ввод имени -> Ввод фамилии -> Ввод отчества
    ---

    :param message: сообщение с фамилией пользователя;
    :param state: Состояние конечного автомата;
    :return:
    """

    # Словарь содержащий данные ТЕКСТ_КНОПКИ : CALLBACK_DATA
    keyboard_structure = {
        "У меня нет отчества": "no_patronymic",
        "Начать сначала": "discount_yes",
        "Отменить и вернуться в главное меню": "cancel",
    }

    await state.update_data(user_entered_last_name=message.text)

    await message.answer(
        text="Отлично, теперь введите ваше отчество\n\n"
             "<b>Внимание, указывайте свое настоящее отчество, иначе заявка будет отклонена оператором!</b>",
        reply_markup=get_inline_keyboard(keyboard_structure, 1, 1),
    )

    await state.set_state(DiscountRegistration.entering_patronymic)


@router.callback_query(F.data == "no_patronymic")
async def discount_no_patronymic_handler(callback: CallbackData, state: FSMContext) -> None:
    """
    Handler, для обработки события, если у пользователя нет отчества.

    ---
    /start -> Хочу скидку! 💸 -> ДА! -> Ввод имени -> Ввод фамилии -> Ввод отчества -> У меня нет отчества
    ---

    :param callback: Callback, полученный после нажатия пользователем inline кнопки;
    :param state: Состояние конечного автомата;
    :return:
    """

    await state.update_data(user_entered_patronymic="Отчество отсутствует")

    user_id = callback.from_user.id

    await bot.send_message(
        chat_id=user_id,
        text="Осталось уточнить только последнюю деталь! Пожалуйста, введите ваш номер телефона\n\n"
             "<b>Внимание, указывайте свой настоящий номер телефона, иначе заявка будет отклонена оператором!</b>",
        reply_markup=get_inline_keyboard(DEFAULT_DISCOUNT_REGISTRATION_KEYBOARD_STRUCTURE, 1, 1),
    )

    await state.set_state(DiscountRegistration.entering_phone_number)


@router.message(DiscountRegistration.entering_patronymic)
async def discount_entered_patronymic_handler(message: types.Message, state: FSMContext) -> None:
    """
    Handler для обработки сообщения с отчеством пользователя.

    ---
    /start -> Хочу скидку! 💸 -> ДА! -> Ввод имени -> Ввод фамилии -> Ввод отчества -> (У меня нет отчества) ->
    -> Ввод номера телефона
    ---

    :param message: сообщение с отчеством пользователя;
    :param state: Состояние конечного автомата;
    :return:
    """

    await state.update_data(user_entered_patronymic=message.text)

    await message.answer(
        text="Осталось уточнить только последнюю деталь! Пожалуйста, введите ваш номер телефона\n\n"
             "<b>Внимание, указывайте свой настоящий номер телефона, иначе заявка будет отклонена оператором!</b>",
        reply_markup=get_inline_keyboard(DEFAULT_DISCOUNT_REGISTRATION_KEYBOARD_STRUCTURE, 1, 1),
    )

    await state.set_state(DiscountRegistration.entering_phone_number)


@router.message(DiscountRegistration.entering_phone_number)
async def discount_entered_phone_number_handler(message: types.Message, state: FSMContext) -> None:
    """
    Handler для обработки сообщения с номером телефона пользователя, а также проверки корректности введенных им
    данных.

    ---
    /start -> Хочу скидку! 💸 -> ДА! -> Ввод имени -> Ввод фамилии -> Ввод отчества -> (У меня нет отчества) ->
    -> Ввод номера телефона -> Подтверждение введенных данных
    ---

    :param message: сообщение с номером телефона пользователя;
    :param state: Состояние конечного автомата;
    :return:
    """

    is_number_correct = phone_num_validator(message.text)

    if is_number_correct:
        await state.update_data(user_entered_phone_number=message.text)

        user_data = await state.get_data()

        # Словарь содержащий данные ТЕКСТ_КНОПКИ : CALLBACK_DATA
        keyboard_structure = {
            "Все верно!": "data_is_correct",
            "Начать сначала": "discount_yes",
        }

        await message.answer(
            text="Пожалуйста, проверьте корректность введенных вами данных.\n\n"
                 "<i>Если вы допустили ошибку, пожалуйста, заполните данные заново.</i>",
        )

        user_data_string = generate_user_data(user_data)

        await message.answer(
            text=user_data_string,
            reply_markup=get_inline_keyboard(keyboard_structure, 1, 1),
        )

        await state.set_state(DiscountRegistration.checking_entered_data)

    else:
        await message.answer(
            text="Введенный номер некорректен! Пожалуйста, введите корректный номер телефона.\n\n"
                 "<b>Внимание, указывайте свой настоящий номер телефона, иначе заявка будет отклонена оператором!</b>",
            reply_markup=get_inline_keyboard(DEFAULT_DISCOUNT_REGISTRATION_KEYBOARD_STRUCTURE, 1, 1),
        )


@router.callback_query(DiscountRegistration.checking_entered_data, F.data == "data_is_correct")
async def discount_data_is_correct_handler(callback: CallbackData, state: FSMContext) -> None:
    """
    Handler, для обработки события, если пользователь подтвердил, что данные корректны.

    ---
    /start -> Хочу скидку! 💸 -> ДА! -> Ввод имени -> Ввод фамилии -> Ввод отчества -> (У меня нет отчества) ->
    -> Ввод номера телефона -> Подтверждение введенных данных -> Данные совпадают
    ---

    :param callback: Callback, полученный после нажатия пользователем inline кнопки;
    :param state: Состояние конечного автомата;
    :return:
    """
    user_id = callback.from_user.id
    user_telegram_username = callback.from_user.username
    user_data = await state.get_data()

    user_data_string = generate_user_data(user_data)

    user_data_string += f"\nTelegram username: @{user_telegram_username}"

    first_name = callback.from_user.first_name

    await bot.send_message(
        chat_id=user_id,
        text="Ваша заявка успешно передана в обработку! Мы обязательно оповестим вас, как только закончим проверку!\n\n"
             "Спасибо за то, что выбрали нас ❤!"
    )

    await bot.send_message(
        chat_id=user_id,
        text=bot_message_texts.MAIN_MENU,
    )

    await bot.send_message(
        chat_id=user_id,
        text=bot_message_texts.MAIN_MENU_TEXT % first_name,
        reply_markup=get_inline_keyboard(MAIN_INLINE_KEYBOARD_STRUCTURE)
    )

    await state.set_state(None)

    # Отправляем сообщение в канал с менеджерами.
    await bot.send_message(
        chat_id=MANAGER_CHAT_ID,
        text=bot_message_texts.DISCOUNT_REGISTRATION_APPLICATION % user_data_string
    )

    insert_user_data(username=user_telegram_username, phone_number=user_data.get('user_entered_phone_number'))
