import logging
import asyncio

from aiogram import Bot, Dispatcher

from bot.config import config
import bot.middlewares as _middlewares
import bot.handlers as _handlers
import bot.utils as _utils


async def start():
    logging.basicConfig(level='DEBUG')

    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()

    dp.update.middleware.register(_middlewares.UserServiceMiddleware())
    dp.update.outer_middleware.register(_middlewares.TripServiceMiddleware())

    dp.include_routers(*_handlers.routers)

    try:
        await dp.start_polling(bot)
        await _utils.set_commands(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
