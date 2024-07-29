from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot.callbacks as _callbacks


def answer_invite_keyboard(
    invite_id: str,
    trip_id: str,
) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            text='Принять',
            callback_data=_callbacks.AnswerInviteCallback(invite_id=invite_id, trip_id=trip_id, answer='accept').pack(),
        ),
        InlineKeyboardButton(
            text='Отклонить',
            callback_data=_callbacks.AnswerInviteCallback(invite_id=invite_id, trip_id=trip_id, answer='reject').pack(),
        ),
    ]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
