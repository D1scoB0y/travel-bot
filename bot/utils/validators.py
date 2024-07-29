

def validate_bio(bio: str) -> str:
    if len(bio) > 200:
        return 'Максимальная длина информации о себе - 200 символов'

    return ''


def validate_trip_name(trip_name: str) -> str:
    if not (3 <= len(trip_name) <= 50):
        return 'Длина названия путешествия - от 3 до 50 символов'

    return ''


def validate_trip_note(trip_note: str) -> str:
    if len(trip_note) > 150:
        return 'Длина заметки не должна превышать 150 символов'

    return ''
