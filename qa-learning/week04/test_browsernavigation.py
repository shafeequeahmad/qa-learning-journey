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

@pytest.mark.usefixtures("orangeHRM")
class BaseTest():
    pass

@pytest.mark.browser
class TestExample(BaseTest):

    def test_has_title(self, page: Page):
        '''This test case demonstrates the use of browser navigation methods in Playwright.
        It navigates to the specified URL, clicks on the "Forgot your password?" link,'''
        page.goto(self.url)
        page.get_by_text("Forgot your password?").click()
        page.wait_for_timeout(3000)
        page.go_back() #navigate to the previous page in history
        page.wait_for_timeout(3000)
        page.go_forward() #navigate to the next page in history
        page.wait_for_timeout(3000)
        page.reload() #refresh the page
        page.wait_for_timeout(3000)
       
