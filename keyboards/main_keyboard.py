from aiogram import types


def get_main_keyboard() -> types.InlineKeyboardMarkup:
    kb = [
        [
            types.InlineKeyboardButton(text="Хочу скидку!", callback_data="test"),
            types.InlineKeyboardButton(text="Посмотреть ассортимент", callback_data="test2"),
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb,
    )

    return keyboard
