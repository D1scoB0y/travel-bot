from aiogram import Router, Bot
from aiogram.types import CallbackQuery

import bot.keyboards as _kb
import bot.services as _services
import bot.callbacks as _callbacks
import bot.filters as _filters


router = Router(name='delete_trip')


@router.callback_query(
    _callbacks.DeleteTripRequestCallback.filter(),
    _filters.GetTripIDFromState(),
)
async def handle_delete_trip_request_callback(
    query: CallbackQuery,
    trip_id: str,
) -> None:
    await query.answer()
    await query.message.answer(  # type: ignore
        'Вы точно хотите удалить путешествие?',
        reply_markup=_kb.delete_trip_keyboard(trip_id=trip_id),
    )


@router.callback_query(
    _callbacks.DeleteTripCallback.filter(),
    _filters.GetTripIDFromState(),
)
async def handle_leave_from_trip_callback(
    query: CallbackQuery,
    trip_service: _services.TripService,
    trip_id: str,
) -> None:
    await trip_service.delete_trip(trip_id=trip_id)
    await query.answer()
    await query.message.answer('Путешествие удалено')  # type: ignore
    await query.message.answer('Выберите действие с путешествиями', reply_markup=_kb.trips_keyboard())  # type: ignore
