from playwright.sync_api import sync_playwright
import random
import string
import pytest

@pytest.mark.usefixtures("burl")
class BaseTest:

    def random_email(self,domain="gmail.com"):
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{prefix}@{domain}"

class TestPlaywrightAPI(BaseTest):

    @pytest.mark.api
    @pytest.mark.api_post
    def test_playwright_post_api(self, playwright: sync_playwright):
        email = self.random_email()
        context = playwright.request.new_context(base_url=self.params['baseurl'])
        response = context.post(
            url = "/public/v2/users",
            headers = self.params['headers'],
            data = {
                    'email': email,
                    'name': 'Shafeeque Ahmad',
                    'gender': 'male',
                    'status': 'active'
                    }
            )
        returned_json = response.json()
        assert response.status == 201, f"Expected status code 201, but got {response.status}"

        for key, value in returned_json.items():
            print(f" ====> {key}: {value}")

        self.params['user_id'].append(returned_json['id'])
        print("===> id list", self.params['user_id'])



