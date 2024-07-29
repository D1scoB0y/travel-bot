from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.services as _services
import bot.utils as _utils
import bot.callbacks as _callbacks


router = Router(name='select_trip')


@router.callback_query(_callbacks.GoToTripListCallback.filter())
async def handle_trip_list_callback(
    query: CallbackQuery,
    callback_data: _callbacks.GoToTripListCallback,
    trip_service: _services.TripService,
    state: FSMContext,
) -> None:
    await state.clear()

    trips = await trip_service.get_trips(owner_id=query.from_user.id)

    await query.answer()
    await query.message.edit_text(  # type: ignore
        'Список ваших путешествий',
        reply_markup=_kb.trip_list_keyboard(trips=trips, page=callback_data.page),
    )


@router.callback_query(_callbacks.SelectTripCallback.filter())
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
    await query.message.edit_text(answer, reply_markup=_kb.trip_keyboard())  # type: ignore
