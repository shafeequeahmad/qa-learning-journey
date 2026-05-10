'''
Practice sit: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
'''
import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.usefixtures("orangeHRM")
class BaseTest():
    """Base test class for Playwright or Selenium test suites."""
    pass

@pytest.mark.builtinlocators
class TestExample(BaseTest):
    """Test class for example Playwright page flows."""
    USER = "Admin"
    PASSWORD = "admin123"

    def test_login(self, page: Page):
        """Test case for login."""
        page.goto(self.url)

        #check if page if loaded by checking the title and other elements
        expect(page).to_have_title(re.compile("OrangeHRM"))
        expect(page.get_by_text("Forgot your password?")).to_be_visible()
        expect(page.get_by_role("heading", name="Login")).to_be_visible()
        expect(page.get_by_role('link', name="OrangeHRM, Inc")).to_be_visible()

        user = page.get_by_placeholder("Username")
        password = page.get_by_role('textbox', name="Password")
        login_button = page.get_by_role("button", name="Login")

        expect(user).to_be_visible()
        user.fill(self.USER)

        expect(password).to_be_visible()
        password.fill(self.PASSWORD)

        expect(login_button).to_be_visible()
        login_button.click()

        expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

