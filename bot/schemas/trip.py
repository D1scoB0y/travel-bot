import datetime as dt
from typing import Optional

from pydantic import BaseModel


class TripPreview(BaseModel):
    id: str
    name: str


class Location(BaseModel):
    id: str
    name: str
    arrival_date: dt.datetime
    departure_date: dt.datetime


class TripInfo(BaseModel):
    id: str
    name: str
    note: Optional[str]
    locations: list[Location]


class Invite(BaseModel):
    id: str
    trip_id: str
    trip_name: str
    owner_username: str

    @staticmethod
    def from_orm_invite(orm_invite):
        return Invite(
            id=orm_invite.id,
            trip_id=orm_invite.trip_id,
            trip_name=orm_invite.trip.name,
            owner_username=orm_invite.owner.username,
        )
