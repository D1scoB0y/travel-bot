from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.enums.parse_mode import ParseMode

import bot.utils as _utils
import bot.keyboards as _kb
import bot.services as _services
import bot.filters as _filters


router = Router(name='navigation')


@router.callback_query(_filters.NavigationFilter('main'))
async def handle_move_to_main(
    query: CallbackQuery,
) -> None:
    await query.answer()
    await query.message.edit_text(_utils.generate_main_page_message(), reply_markup=_kb.main_keyboard())  # type: ignore


@router.callback_query(_filters.NavigationFilter('profile'))
async def handle_move_to_profile(
    query: CallbackQuery,
    user_service: _services.UserService,
) -> None:
    profile = await user_service.get_profile(query.from_user.id)

    message = _utils.generate_profile_message(profile)

    await query.answer()
    await query.message.edit_text(message, parse_mode=ParseMode.HTML, reply_markup=_kb.profile_keyboard())  # type: ignore


@router.callback_query(_filters.NavigationFilter('trips'))
async def handle_move_to_trips(
    query: CallbackQuery,
) -> None:
    await query.answer()
    await query.message.edit_text('Выберите действие с путешествиями', reply_markup=_kb.trips_keyboard())  # type: ignore  
