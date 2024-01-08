from aiogram import types


def get_yes_no_keyboard() -> types.InlineKeyboardMarkup:
    """
    Функция для генерации inline клавиатуры с выбором ответа (Да, Нет).

    :return: Возвращает inline клавиатуру (объект типа InlineKeyboardMarkup)
    """

    kb = [
        [
            types.InlineKeyboardButton(text="ДА!", callback_data="discount_yes"),
            types.InlineKeyboardButton(text="Пожалуй позже", callback_data="discount_later"),
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb,
    )

    return keyboard
