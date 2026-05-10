from playwright.sync_api import Page, expect
import pytest

@pytest.mark.usefixtures("practiceURL")
class BaseTest:
    """Base test class for Playwright or Selenium test suites."""
    pass

class TestFillForm(BaseTest):
    """Test class for form filling and submission scenarios."""

    @pytest.mark.form
    def test_fill_form(self, page: Page):
        '''Test to fill out a form and submit it.'''

        page.goto(self.url + "/form-fields/")

        # Fill the name and password fields
        page.get_by_test_id('name-input').fill("Shafeeque Ahmad")
        page.locator('input[type="password"]').fill("xyz123")

        # Select all checkboxes
        page.locator('#drink1').check()
        page.locator('#drink2').check()
        page.locator('#drink3').check()
        page.locator('#drink4').check()
        page.get_by_test_id('drink5').check()

        # select the radio button
        page.locator('#color3').check()

        #select the dropdown option
        drp = page.locator('#automation')
        options = drp.locator('option')
        print(" ====> Total options in dropdown: ", options.count())
        print(" ====> Dropdown options: ", options.all_text_contents())

        page.locator('#automation').select_option('Yes')

        # Fill email address and message
        page.locator('#email').fill("shafeeque.ahmad@example.com")
        page.locator('#message').fill("This is a test message.")

        page.wait_for_timeout(3000)
        # Click the submit button
        page.get_by_role('button', name='Submit').click()
        page.wait_for_timeout(3000)

        # Accept alert
        page.on("dialog", lambda dialog: dialog.accept() if dialog.message == "Message received!" else None)
