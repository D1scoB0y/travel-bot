from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ok_keyboard(callback: str) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            text='Ок',
            callback_data=callback,
        ),
    ]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
