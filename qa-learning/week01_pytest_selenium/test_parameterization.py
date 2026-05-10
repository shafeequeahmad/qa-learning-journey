import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

@pytest.mark.usefixtures("web_driver")
class BaseTest:
    """Base test class for Playwright or Selenium test suites."""
    pass

class TestGoogle(BaseTest):
    """Test class for Google search and title validation."""

    @pytest.mark.parametrize("username, password",
        [
            pytest.param("testuser1", "password1", marks=pytest.mark.parameter),
            pytest.param("testuser2", "password2", marks=pytest.mark.parameter),
        ])
    def test_google_title(self, username, password):
        """Test case for google title."""
        self.driver.get("https://mail.rediff.com/cgi-bin/login.cgi")
        self.driver.find_element(By.ID, "login1").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.NAME, "proceed").click()



