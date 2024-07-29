from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.services as _services
import bot.states as _states
import bot.utils as _utils
import bot.filters as _filters
import bot.callbacks as _callbacks


router = Router(name='rename_trip')


@router.callback_query(_callbacks.RenameTripCallback.filter())
async def handle_rename_trip_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.TripActionState.waiting_for_new_name)
    await query.answer()
    await query.message.answer('Введите новое название поездки')  # type: ignore


@router.message(
    _states.TripActionState.waiting_for_new_name,
    F.text,
    _filters.GetTripIDFromState(),
)
async def handle_new_valid_trip_name(
    message: Message,
    trip_service: _services.TripService,
    state: FSMContext,
    trip_id: str,
) -> None:
    trip = await trip_service.rename_trip(
        trip_id=trip_id,
        owner_id=message.from_user.id,  # type: ignore
        new_name=message.text,          # type: ignore
    )

    answer = _utils.generate_trip_message(trip)

    await state.set_state(state=None)
    await message.answer(f'Название путешествия изменено на {message.text}')
    await message.answer(answer, reply_markup=_kb.trip_keyboard())


@router.message(_states.TripActionState.waiting_for_new_name)
async def handle_new_invalid_trip_name(message: Message) -> None:
    await message.answer('Ожидается новое название путешествия')
