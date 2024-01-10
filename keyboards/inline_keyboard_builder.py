"""
Модуль для построения inline клавиатуры.


Автор: danisimore
Дата: 10.01.2024


Функция реализованная в данном модуле возвращает inline клавиатуру (объект типа InlineKeyboardMarkup).
Принимает параметр buttons_dict, который является словарем и содержит в себе данные вида ТЕКСТ_КНОПКИ : CALLBACK_DATA.

Также принимает *args - должны быть числа, используются для разметки клавиатуры (кол-во чисел - это кол-во рядов,
значение числа - кол-во кнопок в ряду).

Путем итерации item'ов словаря формируется клавиатура с текстом кнопки и callback'ом. После цикла у объекта builder
вызывается метод adjust, которому в кач-ве аргумента передается args.
"""

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard(buttons_dict: dict, *args) -> types.InlineKeyboardMarkup:
    """
    Строит inline клавиатуру.

    :param buttons_dict: словарь с парами текст_кнопки:callback
    :param args: числа(int) - разметка (сколько кнопок в одном ряду)
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
