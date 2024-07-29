from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot.callbacks as _callbacks


def trips_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Новое путешествие',
                callback_data=_callbacks.CreateTripCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Мои путешествия',
                callback_data=_callbacks.GoToTripListCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Приглашения',
                callback_data=_callbacks.GoToInviteListCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Путешествия друзей',
                callback_data=_callbacks.GoToFriendsTripsListCallback().pack(),
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
