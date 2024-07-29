from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import bot.services as _services
import bot.keyboards as _kb
import bot.states as _states
import bot.utils as _utils
import bot.callbacks as _callbacks


router = Router(name='change_bio')


@router.callback_query(_callbacks.ChangeBIOCallback.filter())
async def handle_change_bio_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(_states.ProfileState.WAITING_FOR_NEW_BIO)
    await query.answer()
    await query.message.answer('Расскажите о себе (до 200 символов)')  # type: ignore


@router.message(
    F.text,
    _states.ProfileState.WAITING_FOR_NEW_BIO
)
async def handle_new_valid_bio(
    message: Message,
    user_service: _services.UserService,
    state: FSMContext,
) -> None:
    profile = await user_service.change_bio(
        user_id=message.from_user.id,  # type: ignore
        bio=message.text,              # type: ignore
    )

    answer = _utils.generate_profile_message(profile)

    await state.clear()
    await message.answer('Информация успешно изменена!')
    await message.answer(answer, reply_markup=_kb.profile_keyboard())


@router.message(_states.ProfileState.WAITING_FOR_NEW_BIO)
async def handle_new_invalid_bio(message: Message) -> None:
    await message.answer('Ожидается текст до 200 символов в длину')
