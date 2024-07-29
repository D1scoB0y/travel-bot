from aiogram.fsm.state import StatesGroup, State


class TripActionState(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_new_note = State()
    waiting_for_location_name = State()
    waiting_for_location_dates = State()
    waiting_for_location_delete_id = State()
    waiting_for_tripmate_username = State()
