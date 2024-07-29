import pytest
import bot.utils as _utils


@pytest.mark.parametrize(
    'bio, is_valid',
    [
        ('', True),
        ('KDJFV*JJ*JSF*', True),
        ('1' * 201, False),
    ],
)
def test_bio_validator(bio: str, is_valid: bool):
    validate_error = _utils.validate_bio(bio)

    assert not bool(validate_error) == is_valid


@pytest.mark.parametrize(
    'trip_name, is_valid',
    [
        ('', False),
        ('11', False),
        ('KDJFV*JJ*JSF*', True),
        ('1' * 51, False),
    ],
)
def test_trip_name_validator(trip_name: str, is_valid: bool):
    validate_error = _utils.validate_trip_name(trip_name)

    assert not bool(validate_error) == is_valid


@pytest.mark.parametrize(
    'trip_note, is_valid',
    [
        ('', True),
        ('KDJFV*JJ*JSF*', True),
        ('1' * 151, False),
    ],
)
def test_trip_note_validator(trip_note: str, is_valid: bool):
    validate_error = _utils.validate_trip_note(trip_note)

    assert not bool(validate_error) == is_valid
