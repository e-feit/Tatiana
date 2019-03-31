import pytest

from app.shared.tatiana_exception import TatianaException
from app.pages.scheduling.scheduling import validate_time

valid_times_data_provider = [
    '12:34:56',
    '00:00:00'
]

@pytest.mark.parametrize('input', valid_times_data_provider)
def test_valid_times(input):
    validate_time(input)

invalid_times_data_provider = [
    '',
    'sdfdf',
    '1111',
    '11:11',
    '11:11:1',
    '11:gg:11',
    'sdf11:11:11sdf',
    '65:00:01',
    '-12:34:56',
]

@pytest.mark.parametrize('input', invalid_times_data_provider)
def test_invalid_times(input):
    with pytest.raises(TatianaException):
        validate_time(input)