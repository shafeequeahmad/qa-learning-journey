
from playwright.sync_api import Page
from constants import app_constants as constants

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = {
            "username_input": "input[name='username']",
            "password_input": "input[name='password']",
            "login_button": "button[type='submit']",
        }

    def login(self):
        self.page.goto(f"{constants.BASE_URL}/auth/login")
        self.page.fill(self.locators["username_input"], constants.USERNAME)
        self.page.fill(self.locators["password_input"], constants.PASSWORD)
        self.page.click(self.locators["login_button"])
        self.page.wait_for_load_state("networkidle")
