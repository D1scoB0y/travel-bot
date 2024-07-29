from aiogram import Router
from aiogram.types import CallbackQuery

import bot.keyboards as _kb
import bot.services as _services
import bot.callbacks as _callbacks


router = Router(name='leave_from_trip')


@router.callback_query(_callbacks.LeaveFromFriendTripCallback.filter())
async def handle_leave_from_trip_callback(
    query: CallbackQuery,
    callback_data: _callbacks.LeaveFromFriendTripCallback,
    trip_service: _services.TripService,
) -> None:
    await trip_service.leave_from_trip(user_id=query.from_user.id, trip_id=callback_data.trip_id)

    trips = await trip_service.get_friends_trips(user_id=query.from_user.id)

    await query.answer()
    await query.message.answer('Вы покинули путешествие')  # type: ignore
    await query.message.answer(                            # type: ignore
        'Список путешествий в которых вы состоите',
        reply_markup=_kb.trip_list_keyboard(trips=trips, page=1, friend_trips=True),
    )
