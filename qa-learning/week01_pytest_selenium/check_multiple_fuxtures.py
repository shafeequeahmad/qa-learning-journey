import pytest


@pytest.fixture
def user():
    """Fixture that provides a test user object for account verification."""
    print("--> Creating user fixture")
    return "Shafeeque"

@pytest.fixture
def balance():
    """Fixture that provides test account balance data."""
    print("--> Creating balance fixture")
    return 100

def test_account(balance, user):
    """Test case for account."""
    print(" --> test_account")
    assert user == "Shafeeque"
    assert balance == 100