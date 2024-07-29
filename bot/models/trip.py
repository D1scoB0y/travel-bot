import datetime as dt
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User
import bot.db as _db
import bot.utils as _utils


class TripMate(_db.Base):
    __tablename__ = 'tripmates'

    id: Mapped[str] = mapped_column(
        sa.String(8),
        primary_key=True,
        index=True,
        default=_utils.generate_id,
    )
    user_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey('users.id'))
    trip_id: Mapped[str] = mapped_column(sa.String(8), sa.ForeignKey('trips.id'))


class Trip(_db.Base):
    __tablename__ = 'trips'

    id: Mapped[str] = mapped_column(
        sa.String(8),
        primary_key=True,
        index=True,
        default=_utils.generate_id,
    )
    name: Mapped[str] = mapped_column(sa.String(50))
    owner_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey('users.id'))
    note: Mapped[Optional[str]]
    locations: Mapped[list["Location"]] = relationship(lazy='selectin', order_by='Location.arrival_date')
    owner: Mapped["User"] = relationship(lazy='joined', foreign_keys=[owner_id])


class Location(_db.Base):
    __tablename__ = 'locations'

    id: Mapped[str] = mapped_column(
        sa.String(8),
        primary_key=True,
        index=True,
        default=_utils.generate_id,
    )
    name: Mapped[str] = mapped_column(sa.String(50))
    trip_id: Mapped[str] = mapped_column(sa.String(8), sa.ForeignKey('trips.id'))
    arrival_date: Mapped[dt.date]
    departure_date: Mapped[dt.date]
    lat: Mapped[float]
    lon: Mapped[float]


class Invite(_db.Base):
    __tablename__ = 'invites'

    id: Mapped[str] = mapped_column(
        sa.String(8),
        primary_key=True,
        index=True,
        default=_utils.generate_id,
    )
    trip_id: Mapped[str] = mapped_column(sa.String(8), sa.ForeignKey('trips.id'))
    owner_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey('users.id'))
    tripmate_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey('users.id'))
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now(dt.timezone.utc).replace(tzinfo=None))

    owner: Mapped["User"] = relationship(foreign_keys=[owner_id], lazy='selectin')
    trip: Mapped["Trip"] = relationship(lazy='selectin')
