from aiogram import types


def get_cancel_keyboard() -> types.InlineKeyboardMarkup:
    """
    Генерирует inline клавиатуру для отмены действий.

    :return: Возвращает inline клавиатуру (объект типа InlineKeyboardMarkup)
    """

    kb = [
        [
            types.InlineKeyboardButton(text="Отменить и вернуться в главное меню", callback_data="cancel"),
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb,
    )

    return keyboard
