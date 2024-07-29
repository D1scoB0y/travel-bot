from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot.callbacks as _callbacks


def profile_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Изменить возраст',
                callback_data=_callbacks.ChangeAgeCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Обновить локацию',
                callback_data=_callbacks.UpdateLocationCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Изменить BIO',
                callback_data=_callbacks.ChangeBIOCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='<< Назад',
                callback_data=_callbacks.NavigationCallback(destination='main').pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
