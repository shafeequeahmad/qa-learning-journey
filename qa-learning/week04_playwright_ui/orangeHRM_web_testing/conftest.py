import pytest

@pytest.fixture(scope='class')
def orangeHRM(request):
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    request.cls.url = url
    return url
