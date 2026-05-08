'''
Practice sit: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
'''
import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.usefixtures("orangeHRM")
class BaseTest():
    pass

@pytest.mark.locator
class TestExample(BaseTest):
    '''This test case demonstrates the use of locators in Playwright.
    It navigates to the specified URL, locates various elements on the page using both relative CSS 
    and relative XPath locators, and performs actions such as filling in the username and password fields 
    and clicking the login button.'''
    
    USER = "Admin"
    PASSWORD = "admin123"

    def test_login(self, page: Page):
        '''This test case demonstrates the use of locators in Playwright.
        It navigates to the specified URL, locates various elements on the page using both relative CSS 
        and relative XPath locators, and performs actions such as filling in the username and password fields 
        and clicking the login button.'''
        page.goto(self.url)
        
        #check if page if loaded by checking the title and other elements
        expect(page).to_have_title(re.compile("OrangeHRM"))
        expect(page.locator(".oxd-text.oxd-text--p.orangehrm-login-forgot-header")).to_be_visible() #relative CSS used
        expect(page.locator("//p[@class='oxd-text oxd-text--p orangehrm-login-forgot-header']")).to_be_visible() #reative xpath used
        
        expect(page.locator(".oxd-text.oxd-text--h5.orangehrm-login-title")).to_be_visible() #relative CSS used
        expect(page.locator("//h5[@class='oxd-text oxd-text--h5 orangehrm-login-title']")).to_be_visible() #reative xpath used
        expect(page.locator("a[href='http://www.orangehrm.com']")).to_be_visible() #relative CSS used
        expect(page.locator("//a[normalize-space()='OrangeHRM, Inc']")).to_be_visible() #reative xpath used

        user = page.locator("//input[@placeholder='Username']") #reative xpath used
        password = page.locator("//input[@placeholder='Password']") #reative xpath used
        login_button = page.locator("//button[@type='submit']") #reative xpath used

        expect(user).to_be_visible()
        user.fill(self.USER)
        
        expect(password).to_be_visible()
        password.fill(self.PASSWORD)
        
        expect(login_button).to_be_visible()
        login_button.click()

        expect(page.locator("//h6[@class='oxd-text oxd-text--h6 oxd-topbar-header-breadcrumb-module']")).to_be_visible()

