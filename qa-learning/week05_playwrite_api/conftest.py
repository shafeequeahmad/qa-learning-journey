# Video link: https://www.youtube.com/watch?v=MumoJxPVZzA&list=PLQKDzuA2cCjpXjzKvUOfvJaWGl9dBWOVo&index=6
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='class')
def burl(request, playwright: sync_playwright):


    params = {
    'baseurl': 'https://gorest.co.in',
    'headers': {"Authorization": "Bearer bbd12c4743b4ded3539ddf251c19f80c5dd677df9b722b0d0e1e86a93ee1b42d"},
    'user_id': []
    }

    # Storing all values for PUT,PATCH and DELETE operations
    context = playwright.request.new_context(base_url=params['baseurl'])
    response = context.get(
            url = "/public/v2/users",
            headers = params['headers']
            )
    for x in response.json():
        params['user_id'].append(x['id'])

    request.cls.params = params
    return params
