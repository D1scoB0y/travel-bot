from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot.callbacks as _callbacks


def delete_trip_keyboard(trip_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Да',
                callback_data=_callbacks.DeleteTripCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data=_callbacks.SelectTripCallback(trip_id=trip_id).pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
