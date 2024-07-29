from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

import bot.db as _db
import bot.schemas as _schemas


class User(_db.Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, index=True)
    registration_stage: Mapped[_schemas.RegistrationStagesEnum] = mapped_column(
        default=_schemas.RegistrationStagesEnum.waiting_for_age,
    )
    username: Mapped[str] = mapped_column(unique=True, index=True)
    bio: Mapped[Optional[str]] = mapped_column(sa.String(200))
    age: Mapped[Optional[int]]
    country: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    lat: Mapped[Optional[float]]
    lon: Mapped[Optional[float]]
