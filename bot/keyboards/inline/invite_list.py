from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

import bot.schemas as _schemas
import bot.callbacks as _callbacks


def invite_list_keyboard(
    invites: list[_schemas.Invite],
    page: int,
) -> InlineKeyboardMarkup:
    invite_list = InlineKeyboardBuilder()

    start = (page - 1) * 4
    end = page * 4

    for invite in invites[start:end]:
        invite_list.button(
            text='@' + invite.owner_username + ' | ' + invite.trip_name,
            callback_data=_callbacks.SelectInviteCallback(
                invite_id=invite.id,
                owner_username=invite.owner_username,
                trip_name=invite.trip_name,
                trip_id=invite.trip_id,
            ),
        )

    invite_list.adjust(1)

    pagination = InlineKeyboardBuilder()

    if page > 1:
        pagination.button(
            text='<<',
            callback_data=_callbacks.GoToInviteListCallback(page=page-1),
        )

    if page < len(invites) / 4:
        pagination.button(
            text='>>',
            callback_data=_callbacks.GoToInviteListCallback(page=page+1)
        )

    pagination.adjust(2)

    back = InlineKeyboardBuilder()

    back.button(text='<< Назад', callback_data=_callbacks.NavigationCallback(destination='trips'))

    invite_list.attach(pagination)
    invite_list.attach(back)

    return invite_list.as_markup()
