import pytest
import requests
from .const import pages

@pytest.mark.usefixtures('baseurl')
class Base:
    """Base class that provides shared configuration for API tests."""
    pass

class TestAPI(Base):
    """Test class for REST API get/post/put/patch operations."""

    def test_get_returns_200(self):
        """Test case for get returns 200."""
        r = requests.get(
            self.params['baseurl'] + '/users?page=1',
            headers=self.params['headers'])
        print("===> test_get_returns_200 <====", r.status_code)
        print("Response JSON:", r.json())
        assert r.status_code == 200, "Status code is not 200."


    def test_response_time_under_3s(self):
        """Test case for response time under 3s."""
        r = requests.get(
            self.params['baseurl'] + '/users',
            headers=self.params['headers'])
        assert r.elapsed.total_seconds() < 3.0

    def test_404_for_unknown_resource(self):
        """Test case for 404 for unknown resource."""
        r = requests.get(
            self.params['baseurl'] + '/users/999999',
            headers=self.params['headers'])
        assert r.status_code == 404

    @pytest.mark.parametrize('page', pages)
    def test_pagination_works(self, page):
        """Test case for pagination works."""
        r = requests.get(
            self.params['baseurl'] + '/users?page=' + str(page),
            headers=self.params['headers'])
        assert r.status_code == 200
        print (">>>>>>>", r.json()['total_pages'])

    def test_get_returns_200(self):
        """Test case for get returns 200."""
        r = requests.get(
            self.params['baseurl'] + '/users',
            headers=self.params['headers'])
        print("===> test_get_returns_200 <====", r.status_code)
        assert r.status_code == 200, "Status code is not 200."
        assert "data" in r.json(), "Expected data not found in response"

    def test_post_create_user(self):
        """Test case for post create user."""
        payload = {"name": "Shafeeque", "job": "Principal QA Engineer"}
        r = requests.post(self.params['baseurl'] + "/users",
                          headers=self.params['headers'],
                          json=payload)
        assert r.status_code == 201   # Created
        assert r.json()["name"] == "Shafeeque"

    def test_put_update_user(self):
        """Test case for put update user."""
        payload = {"name": "Shafeeque", "job": "Senior QA"}
        r = requests.put(self.params['baseurl'] + "/users/2",
                         headers=self.params['headers'],
                         json=payload)
        assert r.status_code == 200
        assert r.json()["job"] == "Senior QA"

    def test_delete_user(self):
        """Test case for delete user."""
        r = requests.delete(self.params['baseurl'] + "/users/2",
                            headers=self.params['headers'])
        assert r.status_code == 204