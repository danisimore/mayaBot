from aiogram import types


def get_main_keyboard() -> types.InlineKeyboardMarkup:
    """
    Функция для генерации inline клавиатуры в главном меню.

    :return: Возвращает inline клавиатуру (объект типа InlineKeyboardMarkup)
    """

    kb = [
        [
            types.InlineKeyboardButton(text="Хочу скидку! 💸", callback_data="discount"),
            types.InlineKeyboardButton(text="Посмотреть ассортимент", callback_data="test2"),
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb,
    )

    return keyboard
