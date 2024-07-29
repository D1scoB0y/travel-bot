from .navigation import router as navigation_router
from .user.start import router as start_router
from .user.change_age import router as change_age_router
from .user.change_bio import router as change_bio_router
from .user.change_location import router as change_location_router
from .trip.select_friends_trip import router as select_fiends_trip_router
from .trip.create_trip import router as create_trip_router
from .trip.leave_from_friend_trip import router as leave_from_trip_router
from .trip.select_trip import router as select_trip_router
from .trip.rename_trip import router as rename_trip_router
from .trip.update_note import router as update_note
from .trip.add_location import router as add_location_router
from .trip.delete_location import router as delete_location_router
from .trip.invite_tripmate import router as invite_tripmate_router
from .trip.select_invite import router as select_invite_router
from .trip.delete_trip import router as delete_trip_router
from .trip.get_direction import router as get_direction_router
from .errors import router as errors_router


routers = [
    errors_router,
    start_router,
    navigation_router,
    change_age_router,
    change_bio_router,
    get_direction_router,
    leave_from_trip_router,
    select_fiends_trip_router,
    change_location_router,
    create_trip_router,
    delete_trip_router,
    select_trip_router,
    rename_trip_router,
    update_note,
    add_location_router,
    delete_location_router,
    invite_tripmate_router,
    select_invite_router,
]
