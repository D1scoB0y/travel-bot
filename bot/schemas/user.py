from enum import Enum

from pydantic import BaseModel


class RegistrationStagesEnum(str, Enum):
    waiting_for_age = 'waiting_for_age'
    waiting_for_location = 'waiting_for_location'
    complete = 'complete'


class UserProfile(BaseModel):
    age: int
    country: str
    city: str
    bio: str | None
