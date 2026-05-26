
from pages.base_page import BasePage
from playwright.sync_api import Page
from constants import app_constants as constants

class ExamplePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = {
            "navigation_menu": "#menu_admin_viewAdminModule",
            "breadcrumbs": "#breadcrumbs",
            "hyperlinks": "#hyperlinks",
            "username_field": "#txtUsername",
            "user_role_dropdown": "#user_role",
            "employee_name_field": "#employee_name",
            "status_dropdown": "#status",
            "search_button": "#searchBtn",
            "reset_button": "#resetBtn",
            "add_button": "#addBtn",
            "table_data": "#table_data",
            "table_headers": "#table_headers",
            "records_found_text": "#records_found_text",
            "actions_column": "#actions_column",
        }
        self.navigate()

    def navigate(self):
        self.login()
        target_url = constants.BASE_URL + "/admin/viewSystemUsers"
        if target_url in self.page.url:
            return
            
        self.page.click("a[href*='admin/viewAdminModule']")
        self.page.wait_for_url("**/admin/viewSystemUsers")

    def verify_navigation_menu(self):
        self.page.goto(f"{constants.BASE_URL}/admin/viewSystemUsers")
        assert self.page.query_selector(self.locators["navigation_menu"]).is_visible()

    def verify_breadcrumbs(self):
        self.page.goto(f"{constants.BASE_URL}/admin/viewSystemUsers")
        assert self.page.query_selector(self.locators["breadcrumbs"]).is_visible()

    def verify_hyperlinks(self):
        self.page.goto(f"{constants.BASE_URL}/admin/viewSystemUsers")
        assert self.page.query_selector(self.locators["hyperlinks"]).is_visible()
