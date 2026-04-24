import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(params=["chrome", "firefox"], scope="class")
def driver(request):
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

@pytest.mark.usefixtures("driver")
class BaseTest:
    pass

class TestGoogle(BaseTest):
    def test_google_title(self):
        self.driver.get("https://www.google.com")
        assert "Google" in self.driver.title

        print(f"Browser used: {self.browser}")
