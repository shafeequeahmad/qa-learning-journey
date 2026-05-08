from playwright.sync_api import sync_playwright
import pytest

@pytest.mark.usefixtures("burl")
class BaseTest:
       pass

class TestPlaywrightAPI(BaseTest):

    @pytest.mark.api
    @pytest.mark.api_get
    def test_playwright_get_api(self, playwright: sync_playwright):
        context = playwright.request.new_context(base_url=self.params['baseurl'])
        response = context.get(
            url = "/public/v2/users",
            headers = self.params['headers']
            )
        returned_json = response.json()
        assert response.status == 200, f"Expected status code 200, but got {response.status}"

        # query params when url is something like https://base_url/users?id=8461018
        response = context.get(
            url = "/public/v2/users",
            params = { 'id' : 8461018 },
            headers = self.params['headers']
            )
        print(" ====> Response JSON: ", response.json(), "\n ====> Response Status: ", response)





