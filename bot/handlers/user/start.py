from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import bot.keyboards as _kb
import bot.states as _states
import bot.schemas as _schemas
import bot.services as _services
import bot.filters as _filters
import bot.utils as _utils


router = Router(name='start')


@router.message(Command('start', 'cancel'))
async def start(message: Message, state: FSMContext, user_service: _services.UserService) -> None:
    await state.clear()
    user = await user_service.get_user_by_id(message.from_user.id)  # type: ignore

    if not user:
        if not message.from_user.username:  # type: ignore
            await message.answer('Для использования этого бота необходимо задать username в настройках Telegram')
            return

        await user_service.create_user(
            user_id=message.from_user.id,  # type: ignore
            username=message.from_user.username,  # type: ignore
            bio=message.chat.bio,  # type: ignore
        )
        await state.set_state(_states.RegistrationState.WAITING_FOR_AGE)
        await message.answer('Укажите ваш возраст')
        return

    if user.registration_stage == _schemas.RegistrationStagesEnum.waiting_for_age:
        await state.set_state(_states.RegistrationState.WAITING_FOR_AGE)
        await message.answer('Укажите ваш возраст')
        return

    if user.registration_stage == _schemas.RegistrationStagesEnum.waiting_for_location:
        await state.set_state(_states.RegistrationState.WAITING_FOR_LOCATION)
        await message.answer('Поделитесь локацией, используя клавиатуру ниже', reply_markup=_kb.share_location_keyboard())
        return

    await message.answer(_utils.generate_main_page_message(), reply_markup=_kb.main_keyboard())


@router.message(
    _states.RegistrationState.WAITING_FOR_AGE,
    _filters.Age(),
)
async def handle_valid_age(
    message: Message,
    user_service: _services.UserService,
    state: FSMContext,
    age: int,
) -> None:
    await user_service.set_age(message.from_user.id, age)  # type: ignore
    await state.set_state(_states.RegistrationState.WAITING_FOR_LOCATION)
    await message.answer('Поделитесь локацией', reply_markup=_kb.share_location_keyboard())


@router.message(_states.RegistrationState.WAITING_FOR_AGE)
async def handle_invalid_age(message: Message) -> None:
    await message.answer(text='Введите ваш возраст')


@router.message(
    _states.RegistrationState.WAITING_FOR_LOCATION,
    _filters.Coordinates(),
)
async def handle_valid_location(
    message: Message,
    user_service: _services.UserService,
    state: FSMContext,
    coordinates: tuple[float, float],
) -> None:
    await user_service.set_location(
        message.from_user.id,  # type: ignore
        coordinates=coordinates,
    )

    await state.clear()
    await message.answer('Регистрация завершена!', reply_markup=ReplyKeyboardRemove())
    await message.answer(_utils.generate_main_page_message(), reply_markup=_kb.main_keyboard())


@router.message(_states.RegistrationState.WAITING_FOR_LOCATION)
async def handle_invalid_location(message: Message) -> None:
    await message.answer('Отправьте корректную геолокацию (используйте клавиатуру ниже)')
