import pytest
from . import constant as const
from playwright.async_api import Page, Route


@pytest.fixture(scope='session')
def burl(request):
    """Provide URL fixture for burl."""
    return const.BASE_URL


