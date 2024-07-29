from aiogram.filters.callback_data import CallbackData


class GoToTripListCallback(CallbackData, prefix='trip-list'):
    page: int = 1


class GoToInviteListCallback(GoToTripListCallback, prefix='invite-list'):
    pass


class GoToFriendsTripsListCallback(GoToTripListCallback, prefix='friends-trips-list'):
    pass


class DeleteTripRequestCallback(CallbackData, prefix='delete-trip-request'):
    pass


class GetDirectionCallback(CallbackData, prefix='get-direction'):
   like_tripmate: bool = False


class DeleteTripCallback(CallbackData, prefix='delete-trip'):
    pass


class SelectTripCallback(CallbackData, prefix='trip'):
    trip_id: str


class LeaveFromFriendTripCallback(CallbackData, prefix='leave-from-trip'):
    trip_id: str


class SelectFriendsTripCallback(CallbackData, prefix='friend-trip'):
    trip_id: str


class RenameTripCallback(CallbackData, prefix='rename-trip'):
    pass


class UpdateNoteCallback(CallbackData, prefix='update-note'):
    pass


class AddLocationCallback(CallbackData, prefix='add-location'):
    pass


class DeleteLocationCallback(CallbackData, prefix='delete-location'):
    pass


class InviteTripmateCallback(CallbackData, prefix='invite-tripmate'):
    pass


class CreateTripCallback(CallbackData, prefix='create-trip'):
    pass


class SelectInviteCallback(CallbackData, prefix='invite'):
    invite_id: str
    owner_username: str
    trip_id: str
    trip_name: str


class AnswerInviteCallback(CallbackData, prefix='answer-invite'):
    invite_id: str
    trip_id: str
    answer: str


class NavigationCallback(CallbackData, prefix='nav'):
    destination: str
