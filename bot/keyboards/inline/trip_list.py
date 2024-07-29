from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

import bot.schemas as _schemas
import bot.callbacks as _callbacks


def trip_list_keyboard(
    trips: list[_schemas.TripPreview],
    page: int,
    friend_trips: bool = False,
) -> InlineKeyboardMarkup:
    trip_list = InlineKeyboardBuilder()

    start = (page - 1) * 4
    end = page * 4

    for trip in trips[start:end]:
        if friend_trips:
            trip_list.button(
                text=trip.name,
                callback_data=_callbacks.SelectFriendsTripCallback(trip_id=trip.id),
            )
        else:
            trip_list.button(
                text=trip.name,
                callback_data=_callbacks.SelectTripCallback(trip_id=trip.id),
            )

    trip_list.adjust(1)

    pagination = InlineKeyboardBuilder()

    if page > 1:
        pagination.button(
            text='<<',
            callback_data=_callbacks.GoToTripListCallback(page=page-1),
        )

    if page < len(trips) / 4:
        pagination.button(
            text='>>',
            callback_data=_callbacks.GoToTripListCallback(page=page+1)
        )

    pagination.adjust(2)

    back = InlineKeyboardBuilder()

    back.button(text='<< Назад', callback_data=_callbacks.NavigationCallback(destination='trips'))

    trip_list.attach(pagination)
    trip_list.attach(back)

    return trip_list.as_markup()
