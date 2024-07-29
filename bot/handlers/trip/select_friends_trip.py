from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.services as _services
import bot.utils as _utils
import bot.callbacks as _callbacks


router = Router(name='select_friends_trip')


@router.callback_query(_callbacks.GoToFriendsTripsListCallback.filter())
async def handle_trip_list_callback(
    query: CallbackQuery,
    callback_data: _callbacks.GoToTripListCallback,
    trip_service: _services.TripService,
    state: FSMContext,
) -> None:
    await state.clear()

    trips = await trip_service.get_friends_trips(user_id=query.from_user.id)

    await query.answer()
    await query.message.edit_text(  # type: ignore
        'Список путешествий в которых вы состоите',
        reply_markup=_kb.trip_list_keyboard(trips=trips, page=callback_data.page, friend_trips=True),
    )


@router.callback_query(_callbacks.SelectFriendsTripCallback.filter())
async def handle_trip_selection_callback(
    query: CallbackQuery,
    callback_data: _callbacks.SelectTripCallback,
    trip_service: _services.TripService,
    state: FSMContext,
) -> None:
    await _utils.set_state_attr(state, 'trip_id', callback_data.trip_id)

    trip = await trip_service.get_trip(trip_id=callback_data.trip_id)  # type: ignore

    answer = _utils.generate_trip_message(trip)

    await query.answer()
    await query.message.edit_text(answer, reply_markup=_kb.friend_trip_keyboard(trip_id=trip.id))  # type: ignore
