from typing import Any
from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update

import bot.db as _db


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_one(self, obj_id: Any, data: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_one(self, obj_id: Any) -> Any:
        raise NotImplementedError()


class SQLAlchemyRepository(AbstractRepository):
    model = _db.Base

    async def add_one(self, data: dict[str, Any]) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                insert(self.model).values(**data),
            )

            await session.commit()

    async def update_one(self, obj_id: Any, data: dict[str, Any]) -> Any:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                update(self.model)
                .values(**data)
                .where(self.model.id == obj_id)  # type: ignore
                .returning(self.model),  
            )

            await session.commit()

            return result.scalar()

    async def get_one(self, obj_id: Any) -> Any:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(self.model)
                .where(self.model.id == obj_id),  # type: ignore
            )

            return result.scalar()
