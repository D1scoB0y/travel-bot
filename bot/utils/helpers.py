from string import ascii_letters, digits
from random import choices
from typing import Any

from aiogram.fsm.context import FSMContext

import bot.schemas as _schemas


def generate_id() -> str:
    return ''.join(choices(ascii_letters + digits, k=8))


def generate_main_page_message() -> str:
    return 'Здравствуйте!\nЯ помогу вам управлять вашими ✈️ путешествиями.'


def generate_profile_message(profile: _schemas.UserProfile) -> str:
    header = 'Ваш профиль\n\n'

    age_section = f'Возраст: {profile.age} лет\n\n'

    country_section = f'Страна: {profile.country}\n\n'

    city_section = f'Город: {profile.city}\n\n'

    bio_section = 'BIO: ' + (profile.bio if profile.bio else 'Не указана')

    message = header + age_section + country_section + city_section + bio_section

    return message


def generate_trip_message(trip: _schemas.TripInfo) -> str:
    message = f'Путешествие: {trip.name}\nID: {trip.id}\n'

    if trip.note:
        message += '\n' + trip.note + '\n'

    if trip.locations:
        message += '\n'

        for index, location in enumerate(trip.locations):
            arrival_date = location.arrival_date.strftime("%d.%m.%Y")
            departure_date = location.departure_date.strftime("%d.%m.%Y")

            message += f'{index+1}) {location.name}\nID: {location.id}\nДата прибытия: {arrival_date}\nДата отбытия: {departure_date}\n\n'

    return message


async def set_state_attr(state: FSMContext, attr: str, value: Any) -> None:
    data = await state.get_data()

    await state.set_data({**data, attr: value})


async def del_state_attr(state: FSMContext, attr: str) -> None:
    data = await state.get_data()

    del data[attr]

    await state.set_data(data)


async def get_state_attr(state: FSMContext, attr: str) -> Any:
    data = await state.get_data()

    return data.get(attr)
