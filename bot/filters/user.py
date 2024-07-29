from aiogram.types import Message
from aiogram.filters import BaseFilter


class Coordinates(BaseFilter):
    async def __call__(self, message: Message) -> dict | bool:
        try:
            return {'coordinates': (message.location.latitude, message.location.longitude)}  # type: ignore
        except:
            return False


class Age(BaseFilter):
    async def __call__(self, message: Message) -> dict | bool:
        try:
            age = message.text

            if not age or not age.isdigit() or int(age) > 150:
                return False

            return {'age': int(age)}
        except:
            return False
