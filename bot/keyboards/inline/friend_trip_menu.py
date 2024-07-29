from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot.callbacks as _callbacks


def friend_trip_keyboard(trip_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Построить маршрут',
                callback_data=_callbacks.GetDirectionCallback(like_tripmate=True).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Покинуть путешествие',
                callback_data=_callbacks.LeaveFromFriendTripCallback(trip_id=trip_id).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='<< Назад',
                callback_data=_callbacks.GoToFriendsTripsListCallback().pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
