from aiogram import Router, F
from aiogram.types import CallbackQuery

import bot.keyboards as _kb
import bot.services as _services
import bot.callbacks as _callbacks


router = Router(name='select_invite')


@router.callback_query(_callbacks.GoToInviteListCallback.filter())
async def handle_invites_list_callback(
    query: CallbackQuery,
    callback_data: _callbacks.GoToInviteListCallback,
    user_service: _services.UserService,
) -> None:
    invites = await user_service.get_invites(user_id=query.from_user.id)

    await query.answer()
    await query.message.edit_text(  # type: ignore
        'Список ваших приглашений',
        reply_markup=_kb.invite_list_keyboard(
            invites=invites,
            page=callback_data.page,
        ),
    )


@router.callback_query(_callbacks.SelectInviteCallback.filter())
async def handle_invite_select_callback(
    query: CallbackQuery,
    callback_data: _callbacks.SelectInviteCallback,
) -> None:
    await query.answer()
    await query.message.edit_text(  # type: ignore
        f'{callback_data.owner_username} приглашает присоединиться к путешествию "{callback_data.trip_name}"',
        reply_markup=_kb.answer_invite_keyboard(invite_id=callback_data.invite_id, trip_id=callback_data.trip_id),
    )


@router.callback_query(_callbacks.AnswerInviteCallback.filter(F.answer == 'accept'))
async def handle_invite_accept_callback(
    query: CallbackQuery,
    callback_data: _callbacks.SelectInviteCallback,
    user_service: _services.UserService,
) -> None:
    await user_service.create_tripmate(user_id=query.from_user.id, trip_id=callback_data.trip_id)
    await user_service.delete_invite(invite_id=callback_data.invite_id)

    invites = await user_service.get_invites(user_id=query.from_user.id)

    await query.answer()
    await query.message.answer(  # type: ignore
        'Приглашение принято. Информация о путешествии появиться во вкладке Путешествия -> Путешествия друзей'
    )
    await query.message.answer(  # type: ignore
        'Список ваших приглашений',
        reply_markup=_kb.invite_list_keyboard(
            invites=invites,
            page=1,
        ),
    )


@router.callback_query(_callbacks.AnswerInviteCallback.filter(F.answer == 'reject'))
async def handle_invite_reject_callback(
    query: CallbackQuery,
    callback_data: _callbacks.SelectInviteCallback,
    user_service: _services.UserService,
) -> None:
    await user_service.delete_invite(invite_id=callback_data.invite_id)

    invites = await user_service.get_invites(user_id=query.from_user.id)

    await query.answer()
    await query.message.answer('Приглашение отклонено')  # type: ignore
    await query.message.answer(                          # type: ignore
        'Список ваших приглашений',
        reply_markup=_kb.invite_list_keyboard(
            invites=invites,
            page=1,
        ),
    )
