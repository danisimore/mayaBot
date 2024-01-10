"""
Модуль генерации главного меню бота.


Автор: danisimore
Дата: 10.01.2024


Функция в данном модуле извлекает id пользователя и его first_name из callback'а и сохраняет значения в переменных.
Далее пользователю отправляются сообщения, текст которых хранится в константах модуля bot_message_texts.
В конце работы функции состояние конечного автомата устанавливается None, т.к. пользователя вернулся в гл. меню.
"""

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

import bot_message_texts


async def show_main_menu_from_callback(
        callback: CallbackData,
        bot: Bot,
        inline_keyboard: InlineKeyboardMarkup,
        state: FSMContext,
) -> None:
    """
    Возвращает пользователя в главное меню.

    :param callback: callback нажатой inline кнопки с данными о пользователе;
    :param bot: объект бота;
    :param inline_keyboard: объект inline клавиатуры;
    :param state: Состояние конечного автомата. Нужно, чтобы установить его в None, в момент возвращения в гл. меню
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
        reply_markup=inline_keyboard
    )

    # Устанавливаем состояние None, т.к. данная функция возвращает пользователя в главное меню.
    await state.set_state(None)
