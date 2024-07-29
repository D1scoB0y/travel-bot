from aiogram.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    WAITING_FOR_AGE = State()
    WAITING_FOR_LOCATION = State()
