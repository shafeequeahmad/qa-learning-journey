import pytest

def is_valid_raid_level(level):
    return level in [0, 1, 5, 6, 10]

@pytest.mark.parametrize('level, expected', [
    (0,  True),
    (1,  True),
    (5,  True),
    (6,  True),
    (10, True),
    (2,  False),
    (3,  False),
    (7,  False),
    (-1, False),
])
@pytest.mark.raid
def test_raid_level_validation(level, expected):
    assert is_valid_raid_level(level) == expected
