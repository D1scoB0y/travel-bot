from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from bot.config import config


async_engine = create_async_engine(config.DB_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

Session = AsyncSession  # alias for AsyncSession type


class Base(DeclarativeBase):
    pass
