from typing import Any 

from aiogram import BaseMiddleware
from aiogram.types import Message

from collections.abc import Callable, Awaitable

from bot.repositories.user import UserRepository
import bot.services as _services


class UserServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        data["user_service"] = _services.UserService(UserRepository())
        return await handler(event, data)
