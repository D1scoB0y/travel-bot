from aiogram import Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import bot.services as _services
import bot.keyboards as _kb
import bot.states as _states
import bot.utils as _utils
import bot.filters as _filters
import bot.callbacks as _callbacks


router = Router(name='change_location')


@router.callback_query(_callbacks.UpdateLocationCallback.filter())
async def handle_change_location_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.ProfileState.WAITING_FOR_NEW_LOCATION)
    await query.answer()
    await query.message.answer('Поделитесь своим местоположением', reply_markup=_kb.share_location_keyboard())  # type: ignore


@router.message(
    _states.ProfileState.WAITING_FOR_NEW_LOCATION,
    _filters.Coordinates(),
)
async def handle_new_valid_location(
    message: Message,
    user_service: _services.UserService,
    state: FSMContext,
    coordinates: tuple[float, float],
) -> None:
    profile = await user_service.change_location(
        message.from_user.id,  # type: ignore
        coordinates=coordinates,
    )

    answer = _utils.generate_profile_message(profile)

    await state.clear()
    await message.answer('Локация успешно изменена!', reply_markup=ReplyKeyboardRemove())
    await message.answer(answer, reply_markup=_kb.profile_keyboard())


@router.message(_states.ProfileState.WAITING_FOR_NEW_LOCATION)
async def handle_new_invalid_location(message: Message) -> None:
    await message.answer('Поделитесь локацией используя клавиатуру ниже')
