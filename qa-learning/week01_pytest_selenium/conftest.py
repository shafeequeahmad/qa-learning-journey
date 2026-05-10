# The fixtur memtioned here is used in test_storage_1.py and test_storage_2.py file.
# It is a session scoped fixture that provides a storage configuration dictionary.
# The fixture can be used in multiple test functions within the same test session,
# and it will be initialized only once.
# The test functions can access the storage configuration by including the fixture name as a parameter.
#
# run test using below cmd
# python -m pytest  -s  -v  -m storage
#
# we can add any number of fixtures in this file and they will be available to all the test files
# in the same directory and subdirectories.

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope='session')
def storage_config():
    """Fixture that returns storage configuration values for tests."""
    return {
        'host': 'localhost',
        'port': 9000,
        'access_key': 'admin',
        'secret_key': 'password123'
    }



@pytest.fixture(params=["chrome", "firefox"], scope="class")
def web_driver(request):
    """Create a Selenium WebDriver instance for the requested browser.

    This fixture initializes a browser driver for either Chrome or Firefox based
    on the current parametrized request value. It attaches the driver instance
    and browser name to the requesting test class so test methods can access them.

    Args:
        request: Pytest fixture request object used to read the current
            parametrized browser value and to attach the driver to the test class.

    Yields:
        WebDriver: A Selenium WebDriver instance for the selected browser.

    After the test class finishes, the fixture quits the browser.
    """
    if request.param == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif request.param == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    request.cls.driver = driver
    request.cls.browser = request.param

    yield driver
    driver.quit()
