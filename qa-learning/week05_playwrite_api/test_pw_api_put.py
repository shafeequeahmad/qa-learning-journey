from playwright.sync_api import sync_playwright
import random
import string
import pytest

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
    @pytest.mark.api_put
    def test_playwright_put_api(self, playwright: sync_playwright):
        """Test to update a user's information using the PUT method."""

        email = self.random_email()
        context = playwright.request.new_context(base_url=self.params['baseurl'])
        name = f'Shafeeque Ahmad khan updated - {email}'
        response = context.put(
            url = f"/public/v2/users/{self.params['user_id'][-1]}",
            headers = self.params['headers'],
            data = {
                    # 'email': email,
                    'name': name,
                    # 'gender': 'male',
                    'status': 'active'
                    }
            )
        returned_json = response.json()
        assert response.status == 200

        print(" ====> Response JSON: ", returned_json)