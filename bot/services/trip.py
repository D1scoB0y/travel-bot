import datetime as dt

import aiohttp
from aiogram.types import BufferedInputFile
from openrouteservice import Client, directions
import folium

from .user import UserService
import bot.utils as _utils
import bot.schemas as _schemas
import bot.repositories as _repos
import bot.exceptions as _exceptions
from bot.config import config


class TripService:
    def __init__(self, repo: _repos.TripRepository) -> None:
        self.repo = repo

    async def create_trip(
        self,
        owner_id: int,
        name: str,
    ) -> None:
        name_validation_error = _utils.validate_trip_name(name)

        if name_validation_error:
            raise _exceptions.BotError(name_validation_error)

        is_name_taken = await self.repo.is_name_taken(owner_id, name)

        if is_name_taken:
            raise _exceptions.BotError('У вас уже есть путешествие с таким названием' )

        await self.repo.create_trip(owner_id=owner_id, name=name)

    async def delete_trip(
        self,
        trip_id: str,
    ) -> None:
        await self.repo.delete_tripmates(trip_id=trip_id)
        await self.repo.delete_invites(trip_id=trip_id)
        await self.repo.delete_locations(trip_id=trip_id)
        await self.repo.delete_trip(trip_id=trip_id)

    async def rename_trip(
        self,
        owner_id: int,
        trip_id: str,
        new_name: str,
    ) -> _schemas.TripInfo:
        name_validation_error = _utils.validate_trip_name(new_name)

        if name_validation_error:
            raise _exceptions.BotError(name_validation_error)

        is_name_taken = await self.repo.is_name_taken(owner_id, new_name)

        if is_name_taken:
            raise _exceptions.BotError('У вас уже есть путешествие с таким названием')

        trip = await self.repo.rename_trip(trip_id=trip_id, new_name=new_name)
        pydantic_trip = _schemas.TripInfo.model_validate(trip, from_attributes=True)

        return pydantic_trip

    async def get_trips(self, owner_id: int) -> list[_schemas.TripPreview]:
        return await self.repo.get_trips(owner_id=owner_id)

    async def get_trip(self, trip_id: str) -> _schemas.TripInfo:
        trip = await self.repo.get_one(trip_id)
        pydantic_trip = _schemas.TripInfo.model_validate(trip, from_attributes=True)
        return pydantic_trip

    async def update_note(self, trip_id: str, new_note: str) -> _schemas.TripInfo:
        note_validation_error = _utils.validate_trip_note(new_note)

        if note_validation_error:
            raise _exceptions.BotError(note_validation_error)

        trip = await self.repo.update_note(trip_id=trip_id, new_note=new_note)
        pydantic_trip = _schemas.TripInfo.model_validate(trip, from_attributes=True)
        return pydantic_trip

    async def location_info(self, location: str) -> dict | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://nominatim.openstreetmap.org/search?city={location}&format=json&accept-language=ru',
            ) as response:
                if response.status != 200:
                    return None

                json = await response.json()

                if not len(json):
                    return None

                return {
                    'name': json[0]['name'],
                    'coords': (float(json[0]['lat']), float(json[0]['lon'])),
                }

    async def add_location(
        self,
        trip_id: str,
        name: str,
        arrival_date: dt.date,
        departure_date: dt.date,
        coords: tuple[float, float],
    ) -> _schemas.TripInfo:
        if arrival_date > departure_date:
            raise _exceptions.BotError('Дата отъезда не может наступить раньше даты прибытия')

        is_date_intersection = await self.repo.is_date_intersection(
            trip_id=trip_id,  # type: ignore
            arrival_date=arrival_date,
            departure_date=departure_date
        )

        if is_date_intersection:
            raise _exceptions.BotError('Пересечение даты пребывания с другой локацией')

        await self.repo.add_location(
            trip_id=trip_id,
            name=name,
            arrival_date=arrival_date,
            departure_date=departure_date,
            coords=coords,
        )

        trip = await self.repo.get_one(trip_id)
        pydantic_trip = _schemas.TripInfo.model_validate(trip, from_attributes=True)
        return pydantic_trip

    async def delete_location(self, location_id: str) -> bool:
        return await self.repo.delete_location(location_id)

    async def get_id_by_username(
        self,
        username: str,
        user_service: UserService,
    ) -> int | None:
        tripmate = await user_service.get_user_by_username(username)

        if not tripmate:
            raise _exceptions.BotError('Пользователя с таким именем не существует')

        return tripmate.id

    async def create_invite(
        self,
        trip_id: str,
        owner_id: int,
        tripmate_id: int,
    ) -> bool:
        invite = await self.repo.get_invite(trip_id=trip_id, tripmate_id=tripmate_id)

        if invite:
            raise _exceptions.BotError('Вы уже пригласили этого пользователя')

        await self.repo.create_invite(trip_id=trip_id, owner_id=owner_id, tripmate_id=tripmate_id)

        return True

    async def get_friends_trips(
        self,
        user_id: int,
    ) -> list[_schemas.TripPreview]:
        return await self.repo.get_friends_trips(user_id=user_id)

    async def leave_from_trip(
        self,
        user_id: int,
        trip_id: str,
    ) -> None:
        await self.repo.delete_tripmate(user_id=user_id, trip_id=trip_id)

    async def build_direction(
        self,
        trip_id: str,
    ) -> BufferedInputFile:
        trip = await self.repo.get_one(trip_id)

        if len(trip.locations) < 1:
            raise _exceptions.BotError('Маршрут можно проложить имея как минимум одну локацию для посещения')

        start_coords = (trip.owner.lat, trip.owner.lon)

        route_waypoints = [start_coords] + [(loc.lat, loc.lon) for loc in trip.locations]

        client = Client(key=config.OPENROUTESERVICE_API_KEY)

        try:
            route_geometry = directions.directions(
                client,
                coordinates=[list(reversed(waypoint)) for waypoint in route_waypoints],
                profile='driving-car',
                format='geojson',
            )
        except:
            raise _exceptions.BotError('Невозможно проложить маршрут.\nВозможные причины:\n1. Две точки разделяет океан.\n2. Длина маршрута более 6000км')

        map_ = folium.Map(
            location=start_coords,
            tiles='OpenStreetMap',
            no_touch=True,
            control_scale=False,
            zoom_control=False,
        )

        folium.PolyLine(
            locations=[list(reversed(coord)) for coord in route_geometry['features'][0]['geometry']['coordinates']],
            color='blue',
        ).add_to(map_)

        map_.fit_bounds(map_.get_bounds(), padding=(10, 10))  # type: ignore

        map_data = _utils.map_image(map_)

        return BufferedInputFile(map_data, filename=f'route_for_trip.{trip_id}.jpg')
