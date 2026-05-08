from playwright.sync_api import sync_playwright
import pytest

@pytest.mark.usefixtures("burl")
class BaseTest:
    pass

class TestPlaywrightAPI(BaseTest):

    @pytest.mark.api 
    @pytest.mark.api_delete
    def test_pw_delete_api(self, playwright: sync_playwright):
        context = playwright.request.new_context(base_url=self.params['baseurl'])
        response = context.delete(
            url = f"/public/v2/users/{self.params['user_id'][-1]}",
            headers = self.params['headers']
        )
        print(">>>>>", response)