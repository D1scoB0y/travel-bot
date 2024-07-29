from aiogram import Router, F
from aiogram.types import ErrorEvent, CallbackQuery, Message
from aiogram.filters import ExceptionTypeFilter

import bot.exceptions as _exceptions
import bot.keyboards as _kb
import bot.utils as _utils


router = Router(name='errors_router')


@router.error(ExceptionTypeFilter(_exceptions.BotError), F.update.message.as_('message'))
async def handle_message_exception(event: ErrorEvent, message: Message):
    await message.answer(event.exception.error)  # type: ignore


@router.error(ExceptionTypeFilter(_exceptions.BotError), F.update.callback_query.as_('query'))
async def handle_query_exception(event: ErrorEvent, query: CallbackQuery):
    await query.answer()
    await query.message.answer(event.exception.error)  # type: ignore
    await query.message.answer(  # type: ignore
        _utils.generate_main_page_message(),
        reply_markup=_kb.main_keyboard(),
    )
