from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.services as _services
import bot.states as _states
import bot.utils as _utils
import bot.keyboards as _kb
import bot.callbacks as _callbacks


router = Router(name='invite_tripmate')


@router.callback_query(_callbacks.InviteTripmateCallback.filter())
async def handle_invite_tripmate_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.TripActionState.waiting_for_tripmate_username)
    await query.answer()
    await query.message.answer('Отметьте пользователя telegram и если он зарегистрирован в нашем боте он получит приглашение на вступление')  # type: ignore


@router.message(
    F.text.startswith('@'),
    _states.TripActionState.waiting_for_tripmate_username,
)
async def handle_valid_tripmate_username_for_invite(
    message: Message,
    trip_service: _services.TripService,
    user_service: _services.UserService,
    state: FSMContext,
    bot: Bot,
) -> None:
    tripmate_id = await trip_service.get_id_by_username(message.text[1:], user_service)  # type: ignore

    trip_id = await _utils.get_state_attr(state, 'trip_id')

    await trip_service.create_invite(
        trip_id=trip_id,                # type: ignore
        owner_id=message.from_user.id,  # type: ignore
        tripmate_id=tripmate_id,        # type: ignore
    )

    trip = await trip_service.get_trip(trip_id)  # type: ignore

    answer = _utils.generate_trip_message(trip)

    await bot.send_message(tripmate_id, f'@{message.from_user.username} приглашает вас учавствовать в путешествии "{trip.name}"\n\n' +  # type: ignore
                           'Принять или отклонить приглашение можно во вкладке Путешествия -> Приглашения')
    await state.set_state(state=None)
    await message.answer(f'Приглашение на вступление в путешестие отправлено пользователю {message.text}')
    await message.answer(answer, reply_markup=_kb.trip_keyboard())


@router.message(_states.TripActionState.waiting_for_tripmate_username)
async def handle_invalid_tripmate_username(message: Message) -> None:
    await message.answer(f'Отметьте пользователя Telegram и мы отправим ему приглашение')
