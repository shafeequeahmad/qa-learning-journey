'''
To generage code with codegen u need to trigger ' playwright codegen "https://playwright.dev/"'
on CLI/terminal. This will open a browser and start recording your actions on the website.
You can then perform various actions like clicking links, filling forms, etc.
The codegen tool will generate the corresponding code for those actions in real-time.
Once you are done, you can stop the recording and save the generated code to a file.
This code can then be used as a test script for automating browser interactions using Playwright.
'''
import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.usefixtures("baseurl")
class BaseTest():
    """Base test class for Playwright or Selenium test suites."""
    pass

@pytest.mark.cls
class TestExample(BaseTest):
    """Test class for example Playwright page flows."""

    def test_has_title(self, page: Page):
        '''This test case demonstrates the use of browser navigation methods in Playwright.
        It navigates to the specified URL, clicks on the "Forgot your password?" link,'''

        page.goto(self.url)

        # Expect a title "to contain" a substring.
        expect(page).to_have_title(re.compile("Playwright"))

    def test_get_started_link(self, page: Page):
        '''This test case demonstrates the use of code generation in Playwright.
        It navigates to the Playwright website, checks for the presence of certain elements,'''

        page.goto(self.url)

        # Click the get started link.
        page.get_by_role("link", name="Get started").click()

        # Expects page to have a heading with the name of Installation.
        expect(page.get_by_role("heading", name="Installation")).to_be_visible()