from pages.base_page import BasePage
from playwright.sync_api import Page
from constants.app_constants import BASE_URL

class DashboardPage(BasePage):
    LOCATORS = {
        "side_menu_items": ".oxd-main-menu-item",
        "widget_names": ".orangehrm-dashboard-widget-name",
        "user_dropdown": ".oxd-userdropdown-tab",
        "brand_logo": ".oxd-brand-banner",
    }

    def __init__(self, page: Page):
        super().__init__(page)
        self.navigate()

    def navigate(self):
        self.login()
        target_url = BASE_URL + "/dashboard/index"
        if target_url in self.page.url:
            return
        
        # Click on Dashboard menu item if not currently on dashboard
        self.page.locator(".oxd-main-menu-item", has_text="Dashboard").click()
        self.page.wait_for_url("**/dashboard/index")

    def get_all_side_menu_texts(self):
        # Wait for elements to be visible
        self.page.wait_for_selector(self.LOCATORS["side_menu_items"])
        items = self.page.locator(self.LOCATORS["side_menu_items"]).all_inner_texts()
        return [item.strip() for item in items if item.strip()]

    def get_all_widget_names(self):
        # Wait for elements to be visible
        self.page.wait_for_selector(self.LOCATORS["widget_names"])
        widgets = self.page.locator(self.LOCATORS["widget_names"]).all_inner_texts()
        return [w.strip() for w in widgets if w.strip()]

    def is_brand_logo_visible(self):
        return self.page.is_visible(self.LOCATORS["brand_logo"])

    def is_user_dropdown_visible(self):
        return self.page.is_visible(self.LOCATORS["user_dropdown"])

