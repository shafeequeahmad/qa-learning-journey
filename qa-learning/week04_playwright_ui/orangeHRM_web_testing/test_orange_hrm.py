from playwright.sync_api import Page, expect
import pytest

@pytest.mark.usefixtures("orangeHRM")
class BaseTest:
    pass

class TestOrangeHRM(BaseTest):

    @pytest.mark.orangehrm
    def test_login(self, page: Page):
        page.goto(self.url)

        # Login to OrangeHRM
        page.fill('input[name="username"]', 'Admin')
        page.fill('input[name="password"]', 'admin123')
        page.click('button[type="submit"]')

        # Validate successful login by checking for the presence of the dashboard
        expect(page.locator('h6')).to_have_text('Dashboard')

        #validate side tabs elements
        if page.locator('i.oxd-icon.bi-chevron-right').is_visible():
            page.locator('i.oxd-icon.bi-chevron-right').click()

        # validate main menu elements
        main_menu = page.locator('ul.oxd-main-menu')
        elements = main_menu.locator('a.oxd-main-menu-item').all_text_contents()

        expected_elements = ['Admin', 'PIM', 'Leave', 'Time', 'Recruitment',
                             'My Info', 'Performance', 'Dashboard', 'Directory',
                             'Maintenance', 'Claim', 'Buzz']
        assert elements == expected_elements, f"Expected {expected_elements} but got {elements}"

        expect(page.locator('div.oxd-sheet.oxd-sheet--rounded.oxd-sheet--white.orangehrm-dashboard-widget')).to_have_count(7)

        list_widget_names = ['Time at Work', 'My Actions', 'Quick Launch',
                             'Buzz Latest Posts', 'Employees on Leave Today',
                             'Employee Distribution by Sub Unit',
                             'Employee Distribution by Location']
        widget_names = page.locator('div.orangehrm-dashboard-widget-name').all_text_contents()

        assert widget_names == list_widget_names, f"Expected {list_widget_names} but got {widget_names}"
        assert len(widget_names) == 7, f"Expected 7 widgets but got {len(widget_names)}"


