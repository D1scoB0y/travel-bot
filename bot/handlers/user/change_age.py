from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.services as _services
import bot.keyboards as _kb
import bot.states as _states
import bot.utils as _utils
import bot.filters as _filters
import bot.callbacks as _callbacks


router = Router(name='change_age')


@router.callback_query(_callbacks.ChangeAgeCallback.filter())
async def handle_change_age_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.ProfileState.WAITING_FOR_NEW_AGE)
    await query.answer()
    await query.message.answer('Введите новый возраст')  # type: ignore


@router.message(
    _states.ProfileState.WAITING_FOR_NEW_AGE,
    _filters.Age(),
)
async def handle_new_valid_age(
    message: Message,
    user_service: _services.UserService,
    state: FSMContext,
    age: int,
) -> None:
    profile = await user_service.change_age(
        user_id=message.from_user.id,  # type: ignore
        age=age,
    )

    answer = _utils.generate_profile_message(profile)

    await state.clear()
    await message.answer('Возраст успешно изменен!')
    await message.answer(answer, reply_markup=_kb.profile_keyboard())


@router.message(_states.ProfileState.WAITING_FOR_NEW_AGE)
async def handle_new_invalid_age(message: Message) -> None:
    await message.answer('Введите корректный возраст')
