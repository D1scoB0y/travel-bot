from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.enums import ChatAction

import bot.keyboards as _kb
import bot.services as _services
import bot.callbacks as _callbacks
import bot.filters as _filters
import bot.utils as _utils


router = Router(name='delete_trip')


@router.callback_query(
    _callbacks.GetDirectionCallback.filter(),
    _filters.GetTripIDFromState(),
)
async def handle_get_direction_callback(
    query: CallbackQuery,
    callback_data: _callbacks.GetDirectionCallback,
    trip_id: str,
    trip_service: _services.TripService,
    bot: Bot,
) -> None:
    await bot.send_chat_action(
        chat_id=query.message.chat.id,  # type: ignore
        action=ChatAction.UPLOAD_PHOTO,
    )

    router_image = await trip_service.build_direction(trip_id=trip_id)

    await query.answer()
    await query.message.answer_photo(  # type: ignore
        photo=router_image,
        caption='Маршрут построен',
    )

    trip = await trip_service.get_trip(trip_id=trip_id)  # type: ignore
    answer = _utils.generate_trip_message(trip)

    await query.message.answer(  # type: ignore
        answer,
        reply_markup=_kb.friend_trip_keyboard(trip_id=trip_id) if callback_data.like_tripmate else _kb.trip_keyboard(),
    )
