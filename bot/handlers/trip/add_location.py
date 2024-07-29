import datetime as dt

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.services as _services
import bot.states as _states
import bot.utils as _utils
import bot.filters as _filters
import bot.callbacks as _callbacks


router = Router(name='add_location')


@router.callback_query(_callbacks.AddLocationCallback.filter())
async def handle_add_location_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.TripActionState.waiting_for_location_name)
    await query.answer()
    await query.message.answer('Введите название любого города который планируете посетить')  # type: ignore


@router.message(
    F.text,
    _states.TripActionState.waiting_for_location_name,
)
async def handle_valid_location_name(
    message: Message,
    trip_service: _services.TripService,
    state: FSMContext,
) -> None:
    info = await trip_service.location_info(location=message.text)  # type: ignore

    if not info:
        await message.answer('Локация с таким названим не найдена')
        return

    await state.set_state(_states.TripActionState.waiting_for_location_dates)
    await _utils.set_state_attr(state, 'location_info', info)
    await message.answer('Введите дату прибытия и отбытия в формате dd.mm.yyyy через пробел (например "10.03.2024 13.03.2024")')


@router.message(_states.TripActionState.waiting_for_location_name)
async def handle_invalid_location_name(message: Message) -> None:
    await message.answer('Ожидается название локации для путешествия')


@router.message(
    _states.TripActionState.waiting_for_location_dates,
    _filters.GetLocationDates(),
    _filters.GetTripIDFromState(),
)
async def handle_valid_location_dates(
    message: Message,
    trip_service: _services.TripService,
    state: FSMContext,
    trip_id: str,
    arrival_date: dt.date,
    departure_date: dt.date,
) -> None:
    info = await _utils.get_state_attr(state, 'location_info')

    trip = await trip_service.add_location(
        trip_id=trip_id,
        name=info['name'],
        arrival_date=arrival_date,
        departure_date=departure_date,
        coords=info['coords'],
    )

    answer = _utils.generate_trip_message(trip)

    await state.set_state(state=None)
    await _utils.del_state_attr(state, 'location_info')
    await message.answer('Локация добавлена!')
    await message.answer(answer, reply_markup=_kb.trip_keyboard())


@router.message(_states.TripActionState.waiting_for_location_dates)
async def handle_invalid_location_dates(message: Message) -> None:
    await message.answer('Ожидаются даты прибытия и отбытия из локации в формате dd.mm.yyyy')
