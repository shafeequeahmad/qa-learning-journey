
from pages.base_page import BasePage
from constants.app_constants import BASE_URL, USERNAME, PASSWORD
from playwright.sync_api import Page

class LoginPage(BasePage):
    LOCATORS = {
        "username_input": "input[name='username']",
        "password_input": "input[name='password']",
        "login_button": "button[type='submit']"
    }

    def __init__(self, page: Page):
        super().__init__(page)
        self.page.goto(BASE_URL + "/auth/login")

    def login(self):
        self.page.fill(self.LOCATORS["username_input"], USERNAME)
        self.page.fill(self.LOCATORS["password_input"], PASSWORD)
        self.page.click(self.LOCATORS["login_button"])
        self.page.wait_for_load_state("networkidle")
