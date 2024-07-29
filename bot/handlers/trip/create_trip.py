from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.services as _services
import bot.states as _states
import bot.callbacks as _callbacks


router = Router(name='create_trip')


@router.callback_query(_callbacks.CreateTripCallback.filter())
async def handle_create_trip_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.CreateTripState.WAITING_FOR_NAME)
    await query.answer()
    await query.message.answer('Введите уникальное название путешествия')  # type: ignore


@router.message(
    _states.CreateTripState.WAITING_FOR_NAME,
    F.text,
)
async def handle_valid_trip_name(
    message: Message,
    trip_service: _services.TripService,
    state: FSMContext,
) -> None:
    await trip_service.create_trip(
        owner_id=message.from_user.id,  # type: ignore
        name=message.text,              # type: ignore
    )

    await state.clear()
    await message.answer(f'Путешествие {message.text} создано! Вы можете найти его во вкладке Мои путешествия', reply_markup=_kb.trips_keyboard())


@router.message(_states.CreateTripState.WAITING_FOR_NAME)
async def handle_invalid_trip_name(message: Message) -> None:
    await message.answer('Ожидается название нового путешествия')
