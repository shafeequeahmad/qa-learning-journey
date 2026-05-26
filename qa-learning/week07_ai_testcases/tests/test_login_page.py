
import pytest
from pages.login_page import LoginPage
from constants.app_constants import BASE_URL
from conftest import browser

@pytest.mark.Smoke
def test_login_page(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    login_page.login()
    assert page.url == BASE_URL + "/dashboard/index"
