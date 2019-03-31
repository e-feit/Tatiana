import pytest

from app.pages.scheduling.scheduling import is_time_valid

data_provider = [
    {'input': '',               'expected_is_valid': False},
    {'input': 'sdfdf',          'expected_is_valid': False},
    {'input': '1111',           'expected_is_valid': False},
    {'input': '11:11',          'expected_is_valid': False},
    {'input': '11:11:1',        'expected_is_valid': False},
    {'input': '11:gg:11',       'expected_is_valid': False},
    {'input': 'sdf11:11:11sdf', 'expected_is_valid': False},
    {'input': '65:00:01',       'expected_is_valid': False},
    {'input': '-12:34:56',      'expected_is_valid': False},

    {'input': '12:34:56',       'expected_is_valid': True},
    {'input': '00:00:00',       'expected_is_valid': True},
]

@pytest.mark.parametrize('data', data_provider)
def test_time_validator(data):
    assert is_time_valid(data['input']) == data['expected_is_valid']