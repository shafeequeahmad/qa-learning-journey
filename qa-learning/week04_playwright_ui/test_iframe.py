from playwright.sync_api import Page, expect
import pytest


@pytest.mark.usefixtures("iframe")
class BaseTest():
    pass

class TestIframe(BaseTest):

    @pytest.mark.iframe
    def test_iframe(self, page: Page):
        '''This test case demonstrates the handling of iframes in Playwright.
        It navigates to a webpage with an iframe, interacts with elements inside the iframe, and verifies the results.'''

        page.goto(self.url)

        # Switch to the iframe using its name or ID.
         # Switch to the iframe using its name or ID.
        frame = page.frame_locator('#iframe-1')

        # Interact with elements inside the iframe.
        frame.get_by_text('Get started').click()
        page.wait_for_timeout(3000)
        frame.locator('a[aria-label="Home page"]').click()
        page.wait_for_timeout(3000)

