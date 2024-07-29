from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot.callbacks as _callbacks


def main_keyboard() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            text='Профиль',
            callback_data=_callbacks.NavigationCallback(destination='profile').pack(),
        ),
        InlineKeyboardButton(
            text='Путешествия',
            callback_data=_callbacks.NavigationCallback(destination='trips').pack(),
        ),
    ]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
