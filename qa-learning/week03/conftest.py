import pytest

@pytest.fixture(scope='class')
def base_url(request):
    params = {
    'baseurl': 'https://reqres.in/api',
    'headers': {"x-api-key": "reqres_542b25491c364ed9aca63b73c1bf95c6"}
    }
    request.cls.params = params

