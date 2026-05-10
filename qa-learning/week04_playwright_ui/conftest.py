import pytest

@pytest.fixture(scope='class')
def baseurl(request):
    """Provide URL fixture for baseurl."""
    url = "https://playwright.dev/"
    request.cls.url = url
    return url

@pytest.fixture(scope='session')
def pwurl():
    """Provide URL fixture for pwurl."""
    url = "https://playwright.dev/"
    print("Setting up the test environment")
    yield url
    print("Tearing down the test environment")

@pytest.fixture(scope='class')
def orangeHRM(request):
    """Fixture that returns the OrangeHRM application URL."""
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    request.cls.url = url
    return url

@pytest.fixture(scope='session')
def jsalert_url():
    """Provide URL fixture for jsalert_url."""
    url = "https://the-internet.herokuapp.com/javascript_alerts"
    yield url

@pytest.fixture(scope='class')
def iframe(request):
    """Fixture that returns the URL used for iframe testing."""
    url = "https://practice-automation.com/iframes/"
    request.cls.url = url
    yield url

@pytest.fixture(scope='class')
def dropdown(request):
    """Fixture that returns the URL used for dropdown interaction tests."""
    url = "https://practice-automation.com/form-fields/"
    request.cls.url = url
    yield url

@pytest.fixture(scope='class')
def tables(request):
    """Fixture that returns the URL for table handling examples."""
    url = "https://practice-automation.com/tables/"
    request.cls.url = url
    yield url

@pytest.fixture(scope='class')
def practiceURL(request):
    """Fixture that returns the practice page base URL for form and dropdown tests."""
    url = "https://practice-automation.com"
    request.cls.url = url
    yield url