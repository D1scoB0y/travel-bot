import datetime as dt

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import BaseFilter

import bot.utils as _utils


class GetTripIDFromState(BaseFilter):
    async def __call__(
        self,
        message: Message,
        state: FSMContext,
    ) -> dict | bool:
        try:
            trip_id = await _utils.get_state_attr(state, 'trip_id')

            return {'trip_id': trip_id}
        except:
            return False


class GetLocationDates(BaseFilter):
    async def __call__(
        self,
        message: Message,
    ) -> dict | bool:
        try:
            arrival_date, departure_date = map(
                lambda x: dt.datetime.strptime(x, '%d.%m.%Y').date(),
                message.text.split(' '),  # type: ignore
            )

            return {
                'arrival_date': arrival_date,
                'departure_date': departure_date,
            }
        except:
            return False


class GetLocationNameFromState(BaseFilter):
    async def __call__(
        self,
        message: Message,
        state: FSMContext,
    ) -> dict | bool:
        try:
            location_name = await _utils.get_state_attr(state, 'location_name')

            return {'location_name': location_name}
        except:
            return False
