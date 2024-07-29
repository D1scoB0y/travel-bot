from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def share_location_keyboard() -> ReplyKeyboardMarkup:
    buttons = [[
        KeyboardButton(
            text='Поделиться локацией',
            request_location=True,
        )
    ]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        one_time_keyboard=True,
        resize_keyboard=True,
    )

    return keyboard
