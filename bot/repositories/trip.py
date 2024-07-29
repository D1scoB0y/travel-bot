import datetime as dt

from sqlalchemy import select, insert, delete

import bot.db as _db
import bot.models as _models
import bot.schemas as _schemas
from .repository import SQLAlchemyRepository


class TripRepository(SQLAlchemyRepository):
    model = _models.Trip

    async def create_trip(self, owner_id: int, name: str) -> None:
        await self.add_one({'owner_id': owner_id, 'name': name})

    async def delete_trip(self, trip_id: str) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                delete(self.model)
                .where(self.model.id == trip_id),
            )

            await session.commit()

    async def is_name_taken(self, owner_id: int, name: str) -> bool:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(self.model.id)
                .where(
                    self.model.name == name,
                    self.model.owner_id == owner_id,
                ),
            )

            return result.scalar() is not None

    async def get_trips(self, owner_id: int) -> list[_schemas.TripPreview]:
        async with _db.async_session_maker() as session:
            trips = await session.execute(
                select(
                    self.model.id,
                    self.model.name,
                )
                .where(
                    self.model.owner_id == owner_id,
                )
            )

            trip_previews = [_schemas.TripPreview.model_validate(
                trip,
                from_attributes=True
            ) for trip in trips.all()]

            return trip_previews

    async def rename_trip(self, trip_id: str, new_name: str) -> _models.Trip:
        return await self.update_one(trip_id, {'name': new_name})

    async def update_note(self, trip_id: str, new_note: str) -> _models.Trip:
        return await self.update_one(trip_id, {'note': new_note})

    async def add_location(
        self,
        trip_id: str,
        name: str,
        arrival_date: dt.date,
        departure_date: dt.date,
        coords: tuple[float, float],
    ) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                insert(_models.Location)
                .values({
                    'name': name,
                    'trip_id': trip_id,
                    'arrival_date': arrival_date,
                    'departure_date': departure_date,
                    'lat': coords[0],
                    'lon': coords[1],
                })
            )

            await session.commit()

    async def is_date_intersection(self, trip_id: str, arrival_date: dt.date, departure_date: dt.date) -> bool:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(
                    _models.Location.id,
                )
                .where(
                    _models.Location.arrival_date < departure_date,
                    _models.Location.departure_date > arrival_date,
                    _models.Location.trip_id == trip_id,
                )
            )

            return result.scalar() is not None

    async def delete_location(self, location_id: str) -> bool:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                delete(_models.Location)
                .where(_models.Location.id == location_id)
            )

            await session.commit()
            return bool(result.rowcount)

    async def get_invite(self, trip_id: str, tripmate_id: int) -> _models.Invite | None:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(_models.Invite)
                .where(
                    _models.Invite.trip_id == trip_id,
                    _models.Invite.tripmate_id == tripmate_id,
                )
            )

            return result.scalar()

    async def create_invite(self, trip_id: str, owner_id: int, tripmate_id: int) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                insert(_models.Invite)
                .values(dict(trip_id=trip_id, owner_id=owner_id, tripmate_id=tripmate_id))
            )

            await session.commit()

    async def get_friends_trips(
        self,
        user_id: int,
    ) -> list[_schemas.TripPreview]:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(
                    self.model.id,
                    self.model.name,
                )
                .join(
                    _models.TripMate,
                    _models.TripMate.trip_id == self.model.id,
                )
                .where(_models.TripMate.user_id == user_id),
            )

            trip_previews = [_schemas.TripPreview.model_validate(
                trip,
                from_attributes=True
            ) for trip in result.all()]

            return trip_previews

    async def delete_tripmate(
        self,
        user_id: int,
        trip_id: str,
    ) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                delete(_models.TripMate)
                .where(
                    _models.TripMate.trip_id == trip_id,
                    _models.TripMate.user_id == user_id,
                )
            )

            await session.commit()

    async def delete_tripmates(
        self,
        trip_id: str,
    ) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                delete(_models.TripMate)
                .where(_models.TripMate.trip_id == trip_id)
            )

            await session.commit()

    async def delete_locations(
        self,
        trip_id: str,
    ) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                delete(_models.Location)
                .where(_models.Location.trip_id == trip_id)
            )

            await session.commit()

    async def delete_invites(
        self,
        trip_id: str,
    ) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                delete(_models.Invite)
                .where(_models.Invite.trip_id == trip_id)
            )

            await session.commit()
