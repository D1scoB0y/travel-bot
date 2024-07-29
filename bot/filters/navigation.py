from aiogram.types import CallbackQuery
from aiogram.filters import BaseFilter


class NavigationFilter(BaseFilter):
    def __init__(self, page: str) -> None:
        self.page = page

    async def __call__(
        self,
        query: CallbackQuery,
    ) -> dict | bool:
        try:
            if not (query.data and query.data.startswith('nav:')):
                return False

            destination = query.data.split(':')[1]

            if destination == self.page:
                return True

            return False
        except:
            return False
