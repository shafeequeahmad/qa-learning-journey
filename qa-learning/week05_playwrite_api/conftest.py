# Video link: https://www.youtube.com/watch?v=MumoJxPVZzA&list=PLQKDzuA2cCjpXjzKvUOfvJaWGl9dBWOVo&index=6
import pytest
from playwright.sync_api import sync_playwright
from .auth import AUTH

@pytest.fixture(scope='class')
def burl(request, playwright: sync_playwright):


    """Provide URL fixture for burl."""
    params = {
    'baseurl': 'https://gorest.co.in',
    'headers': {"Authorization": AUTH},
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
