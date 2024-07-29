from typing import Any
from sqlalchemy import delete, select, desc, insert

import bot.db as _db
from bot.repositories.repository import SQLAlchemyRepository 
import bot.models as _models
import bot.schemas as _schemas


class UserRepository(SQLAlchemyRepository):
    model = _models.User

    async def create_user(self, user_id: int, username: str, bio: str | None) -> None:
        await self.add_one({'id': user_id, 'username': username, 'bio': bio})

    async def set_age(self, user_id: int, age: int) -> Any:
        return await self.update_one(user_id, {'age': age})

    async def set_registration_stage(self, user_id: int, stage: _schemas.RegistrationStagesEnum) -> None:
        await self.update_one(user_id, {'registration_stage': stage})

    async def set_location(
        self,
        user_id: int,
        country: str,
        city: str,
        coords: tuple[float, float],
    ) -> _models.User:
        return await self.update_one(
            user_id,
            {
                'country': country,
                'city': city,
                'lat': coords[0],
                'lon': coords[1],
            }
        )

    async def set_bio(self, user_id: int, bio: str) -> _models.User:
        return await self.update_one(user_id, {'bio': bio})

    async def get_user_by_id(self, user_id: int) -> _models.User | None:
        return await self.get_one(user_id)

    async def get_registration_stage(self, user_id: int) -> _schemas.RegistrationStagesEnum:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(_models.User.registration_stage)
                .where(_models.User.id == user_id),
            )

            return result.scalar_one()

    async def get_profile(self, user_id: int) -> _schemas.UserProfile:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(
                    _models.User.age,
                    _models.User.country,
                    _models.User.city,
                    _models.User.bio,
                )
                .where(
                    _models.User.id == user_id,
                ),
            )

            return _schemas.UserProfile.model_validate(result.one(), from_attributes=True)

    async def get_user_by_username(self, username: str) -> _models.User | None:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(_models.User)
                .where(_models.User.username == username)
            )

            return result.scalar()

    async def get_invites(self, user_id: int) -> list[_schemas.Invite]:
        async with _db.async_session_maker() as session:
            result = await session.execute(
                select(_models.Invite)
                .where(_models.Invite.tripmate_id == user_id)
                .order_by(desc(_models.Invite.created_at))
            )

            invites = [_schemas.Invite.from_orm_invite(
                orm_invite=invite,
            ) for invite in result.scalars().all()]

            return invites

    async def delete_invite(self, invite_id: str) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                delete(_models.Invite)
                .where(_models.Invite.id == invite_id)
            )

            await session.commit()

    async def create_tripmate(self, user_id: int, trip_id: str) -> None:
        async with _db.async_session_maker() as session:
            await session.execute(
                insert(_models.TripMate)
                .values(dict(user_id=user_id, trip_id=trip_id)),
            )

            await session.commit()

