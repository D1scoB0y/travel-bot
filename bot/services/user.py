import aiohttp

from bot.repositories.user import UserRepository
import bot.utils as _utils
import bot.models as _models
import bot.schemas as _schemas
import bot.exceptions as _exceptions


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def create_user(
        self,
        user_id: int,
        username: str,
        bio: str,
    ) -> None:
        await self.repo.create_user(user_id, username=username, bio=bio)

    async def set_age(
        self,
        user_id: int,
        age: int,
    ) -> None:
        registration_stage = await self.repo.get_registration_stage(user_id)

        if registration_stage != _schemas.RegistrationStagesEnum.complete:
            await self.repo.set_registration_stage(user_id, _schemas.RegistrationStagesEnum.waiting_for_location)

        await self.repo.set_age(user_id, age)

    async def change_age(
        self,
        user_id: int,
        age: int,
    ) -> _schemas.UserProfile:
        registration_stage = await self.repo.get_registration_stage(user_id)

        if registration_stage != _schemas.RegistrationStagesEnum.complete:
            await self.repo.set_registration_stage(user_id, _schemas.RegistrationStagesEnum.waiting_for_location)

        updated_user = await self.repo.set_age(user_id, age)

        profile = _schemas.UserProfile.model_validate(updated_user, from_attributes=True)

        return profile

    async def set_location(
        self,
        user_id: int,
        coordinates: tuple[float, float],
    ) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://nominatim.openstreetmap.org/reverse?lat={coordinates[0]}&lon={coordinates[1]}&format=json&accept-language=ru',
            ) as response:
                if response.status != 200:
                    raise _exceptions.BotError('Сторонний сервис не отвечает. Попробуйте позже')

                json_ = await response.json()

                try:
                    country = json_['address']['country']
                    city = json_['address']['city']
                except KeyError:
                    raise _exceptions.BotError('Сторонний сервис ответил некорректно. Попробуйте позже')

                await self.repo.set_location(user_id, country=country, city=city, coords=coordinates)
                await self.repo.set_registration_stage(user_id, _schemas.RegistrationStagesEnum.complete)

    async def change_location(
        self,
        user_id: int,
        coordinates: tuple[float, float],
    ) -> _schemas.UserProfile:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://nominatim.openstreetmap.org/reverse?lat={coordinates[0]}&lon={coordinates[1]}&format=json&accept-language=ru',
            ) as response:
                if response.status != 200:
                    raise _exceptions.BotError('Сторонний сервис не отвечает. Попробуйте позже')

                json_ = await response.json()

                try:
                    country = json_['address']['country']
                    city = json_['address']['city']
                except KeyError:
                    raise _exceptions.BotError('Сторонний сервис ответил некорректно. Попробуйте позже')

                updated_user = await self.repo.set_location(user_id, country=country, city=city, coords=coordinates)

                profile = _schemas.UserProfile.model_validate(updated_user, from_attributes=True)

                return profile

    async def change_bio(
        self,
        user_id: int,
        bio: str,
    ) -> _schemas.UserProfile:
        bio_validation_error = _utils.validate_bio(bio)

        if bio_validation_error:
            raise _exceptions.BotError(bio_validation_error)

        updated_user = await self.repo.set_bio(user_id, bio=bio)

        profile = _schemas.UserProfile.model_validate(updated_user, from_attributes=True)

        return profile

    async def get_registration_stage(self, user_id: int) -> _schemas.RegistrationStagesEnum:
        return await self.repo.get_registration_stage(user_id)

    async def get_user_by_id(self, user_id: int) -> _models.User | None:
        return await self.repo.get_user_by_id(user_id)

    async def get_profile(self, user_id: int) -> _schemas.UserProfile:
        return await self.repo.get_profile(user_id)

    async def get_user_by_username(self, username: str) -> _models.User | None:
        return await self.repo.get_user_by_username(username)

    async def get_invites(self, user_id: int) -> list[_schemas.Invite]:
        return await self.repo.get_invites(user_id=user_id)

    async def delete_invite(self, invite_id: str) -> None:
        await self.repo.delete_invite(invite_id=invite_id)

    async def create_tripmate(self, user_id: int, trip_id: str) -> None:
        await self.repo.create_tripmate(user_id=user_id, trip_id=trip_id)
