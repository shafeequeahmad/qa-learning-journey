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

@pytest.fixture(scope='session')
def jsalert_url():
    url = "https://the-internet.herokuapp.com/javascript_alerts"
    yield url

@pytest.fixture(scope='class')
def iframe(request):
    url = "https://practice-automation.com/iframes/"
    request.cls.url = url
    yield url

@pytest.fixture(scope='class')
def dropdown(request):
    url = "https://practice-automation.com/form-fields/"
    request.cls.url = url
    yield url

@pytest.fixture(scope='class')
def tables(request):
    url = "https://practice-automation.com/tables/"
    request.cls.url = url
    yield url

@pytest.fixture(scope='class')
def practiceURL(request):
    url = "https://practice-automation.com"
    request.cls.url = url
    yield url