from playwright.sync_api import sync_playwright
import pytest
import random
import string

@pytest.mark.usefixtures("burl")
class BaseTest:

    """Base test class for Playwright or Selenium test suites."""

    def random_email(self,domain="gmail.com"):
        """Generate a random email address for test data."""
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{prefix}@{domain}"

class TestPlaywrightAPI(BaseTest):
    """Test class for Playwright API CRUD operations."""

    @pytest.mark.api
    @pytest.mark.api_patch
    def test_playwright_patch_api(self, playwright: sync_playwright):
        """Test to update a user's information using the PATCH method."""

        email = self.random_email()
        context = playwright.request.new_context(base_url=self.params['baseurl'])
        name = f'Shafeeque Ahmad khan updated - {email}'
        response = context.put(
            url = f"/public/v2/users/{self.params['user_id'][-1]}",
            headers = self.params['headers'],
            data = {
                    'email': email,
                    'name': name
                    }
            )
        returned_json = response.json()
        assert response.status == 200, \
            f"Expected status code 200, but got {response.status}"
        assert returned_json['email'] == email, \
              f"Expected email to be updated to {email}, but got {returned_json['email']}"
        assert returned_json['name'] == name, \
              f"Expected name to be updated to {name}, but got {returned_json['name']}"