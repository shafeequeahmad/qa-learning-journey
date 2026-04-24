import pytest


@pytest.fixture
def user():
    print("--> Creating user fixture")
    return "Shafeeque"

@pytest.fixture
def balance():
    print("--> Creating balance fixture")
    return 100

def test_account(balance, user):
    print(" --> test_account")
    assert user == "Shafeeque"
    assert balance == 100