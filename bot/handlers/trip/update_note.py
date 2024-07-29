from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.services as _services
import bot.states as _states
import bot.utils as _utils
import bot.filters as _filters
import bot.callbacks as _callbacks


router = Router(name='update_note')


@router.callback_query(_callbacks.UpdateNoteCallback.filter())
async def handle_update_trip_note_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.TripActionState.waiting_for_new_note)
    await query.answer()
    await query.message.answer('Введите новую заметку (до 150 символов)')  # type: ignore


@router.message(
    _states.TripActionState.waiting_for_new_note,
    F.text,
    _filters.GetTripIDFromState(),
)
async def handle_new_valid_trip_note(
    message: Message,
    trip_service: _services.TripService,
    state: FSMContext,
    trip_id: str,
) -> None:
    trip = await trip_service.update_note(
        trip_id=trip_id,
        new_note=message.text,  # type: ignore
    )

    answer = _utils.generate_trip_message(trip)

    await state.set_state(state=None)
    await message.answer('Заметка обновлена!')
    await message.answer(answer, reply_markup=_kb.trip_keyboard())


@router.message(_states.TripActionState.waiting_for_new_note)
async def handle_new_invalid_trip_note(message: Message) -> None:
    await message.answer('Ожидается новая заметка для путешествия')
