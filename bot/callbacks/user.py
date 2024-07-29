from aiogram.filters.callback_data import CallbackData


class ChangeAgeCallback(CallbackData, prefix='change-age'):
    pass


class UpdateLocationCallback(CallbackData, prefix='update-location'):
    pass


class ChangeBIOCallback(CallbackData, prefix='change-bio'):
    pass
