from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard(buttons_dict: dict, *args) -> types.InlineKeyboardMarkup:
    """
    Строит клавиатуру на основе словаря (ТЕКСТ_КНОПКИ : CALLBACK_DATA). После словаря передаются числа (int),
    Каждое число описывает количество кнопок в ряду.

    :param buttons_dict: словарь с парами текст_кнопки:callback
    :param args: разметка (сколько кнопок в одном ряду)
    :return: Возвращает inline клавиатуру (объект типа InlineKeyboardMarkup)
    """

    # Создаем объект InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()

    # Итерируем словарь
    for button_text, button_callback in buttons_dict.items():
        # Добавляем в builder текст кнопки и ее callback
        builder.add(
            types.InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback,
            )
        )
    builder.adjust(*args)
    # Преобразуем builder в объект InlineKeyboardMarkup
    inline_keyboard = builder.as_markup()

    return inline_keyboard
