from aiogram.fsm.state import StatesGroup, State


class ProfileState(StatesGroup):
    WAITING_FOR_NEW_AGE = State()
    WAITING_FOR_NEW_LOCATION = State()
    WAITING_FOR_NEW_BIO = State()
