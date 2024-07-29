from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.services as _services
import bot.states as _states
import bot.utils as _utils
import bot.callbacks as _callbacks


router = Router(name='delete_location')


@router.callback_query(_callbacks.DeleteLocationCallback.filter())
async def handle_delete_location_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.TripActionState.waiting_for_location_delete_id)
    await query.answer()
    await query.message.answer('Введите ID локации для удаления')  # type: ignore


@router.message(
    F.text,
    _states.TripActionState.waiting_for_location_delete_id,
)
async def handle_location_id_for_delete(
    message: Message,
    trip_service: _services.TripService,
    state: FSMContext,
) -> None:
    trip_id = await _utils.get_state_attr(state, 'trip_id')

    is_deleted = await trip_service.delete_location(
        location_id=message.text,  # type: ignore
    )

    trip = await trip_service.get_trip(trip_id=trip_id)  # type: ignore

    if not is_deleted:
        await message.answer('Локации с таким ID не существует')
        return    

    answer = _utils.generate_trip_message(trip)

    await state.set_state(state=None)
    await message.answer(f'Локация с ID {message.text} удалена')
    await message.answer(answer, reply_markup=_kb.trip_keyboard())
