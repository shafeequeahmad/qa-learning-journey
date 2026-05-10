from playwright.sync_api import Page, expect
import pytest

# Tutorial: https://www.youtube.com/watch?v=FcF__Qehlg4&list=PLBw1ubD1J1UjtoSTM_4o1B9_QAjzXznrL&index=3

@pytest.mark.usefixtures("dropdown")
class BaseTest():
    """Base test class for Playwright or Selenium test suites."""
    pass

class TestDropdown(BaseTest):
    """Test class for dropdown interaction scenarios."""

    @pytest.mark.dropdown
    def test_dropdown(self, page: Page):
        '''This test case demonstrates the handling of dropdowns in Playwright.
        It navigates to a webpage with a dropdown, interacts with the dropdown, and verifies the results.'''

        page.goto(self.url)

        # Interact with the dropdown using select_option.
        dropdown = page.locator('#automation')
        dropdown.scroll_into_view_if_needed()
        options = dropdown.locator('option')
        expect(options).to_have_count(4)
        expected_options = ["default", "yes", "no", "undecided"]

        for i in range(len(expected_options)):
            expect(options.nth(i)).to_have_attribute("value", expected_options[i])

        dropdown.select_option("yes")
        expect(dropdown).to_have_value("yes")
        page.wait_for_timeout(3000)
        dropdown.select_option("no")
        expect(dropdown).to_have_value("no")
        page.wait_for_timeout(3000)


        #checkbox and radio buttons testing
        page.locator('#drink1').click()
        expect(page.locator('#drink1')).to_be_checked()
        page.wait_for_timeout(3000)

        radio_buttons = page.locator('#color3')
        radio_buttons.scroll_into_view_if_needed()
        radio_buttons.click()
        expect(radio_buttons).to_be_checked()
        page.wait_for_timeout(3000)