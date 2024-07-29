from aiogram.fsm.state import StatesGroup, State


class CreateTripState(StatesGroup):
    WAITING_FOR_NAME = State()
