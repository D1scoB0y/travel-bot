from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot.callbacks as _callbacks


def trip_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='Переименовать',
                callback_data=_callbacks.RenameTripCallback().pack(),
            ),
            InlineKeyboardButton(
                text='Изменить заметку',
                callback_data=_callbacks.UpdateNoteCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='+Локация',
                callback_data=_callbacks.AddLocationCallback().pack(),
            ),
            InlineKeyboardButton(
                text='-Локация',
                callback_data=_callbacks.DeleteLocationCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Построить маршрут',
                callback_data=_callbacks.GetDirectionCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Пригласить друга',
                callback_data=_callbacks.InviteTripmateCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Удалить путешествие',
                callback_data=_callbacks.DeleteTripRequestCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='<< Назад',
                callback_data=_callbacks.GoToTripListCallback().pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
