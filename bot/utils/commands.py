from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command='start',
            description='Начать диалог',
        ),
        BotCommand(
            command='cancel',
            description='Отменить действие и вернуться в главное меню',
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
