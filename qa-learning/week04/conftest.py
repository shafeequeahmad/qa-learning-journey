import pytest

@pytest.fixture(scope='class')
def baseurl(request):
    url = "https://playwright.dev/"
    request.cls.url = url
    return url

@pytest.fixture(scope='session')
def pwurl():
    url = "https://playwright.dev/"
    print("Setting up the test environment")
    yield url
    print("Tearing down the test environment")

@pytest.fixture(scope='class')
def orangeHRM(request):
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    request.cls.url = url
    return url