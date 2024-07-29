from typing import Any 

from aiogram import BaseMiddleware
from aiogram.types import Message

from collections.abc import Callable, Awaitable

from bot.repositories.trip import TripRepository
import bot.services as _services


class TripServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        data["trip_service"] = _services.TripService(TripRepository())
        return await handler(event, data)
