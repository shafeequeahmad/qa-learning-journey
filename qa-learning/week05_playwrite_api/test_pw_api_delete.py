from playwright.sync_api import sync_playwright
import pytest

@pytest.mark.usefixtures("burl")
class BaseTest:
    """Base test class for Playwright or Selenium test suites."""
    pass

class TestPlaywrightAPI(BaseTest):
    """Test class for Playwright API CRUD operations."""

    @pytest.mark.api
    @pytest.mark.api_delete
    def test_playwright_delete_api(self, playwright: sync_playwright):
        """Test case for playwright delete api."""
        context = playwright.request.new_context(base_url=self.params['baseurl'])
        response = context.delete(
            url = f"/public/v2/users/{self.params['user_id'][-1]}",
            headers = self.params['headers']
        )
        print(">>>>>", response)