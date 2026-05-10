# from tkinter import dialog

from playwright.sync_api import Page, expect
import pytest

# Tutorial: https://www.youtube.com/watch?v=CA2mLA8o3GQ&list=PLBw1ubD1J1UjtoSTM_4o1B9_QAjzXznrL&index=5

@pytest.mark.jsalert
def test_jsalerts(page: Page, jsalert_url):
        '''This test case demonstrates the handling of JavaScript alerts in Playwright.
        It navigates to a webpage with JavaScript alerts, interacts with the alerts, and verifies the results.'''

        page.goto(jsalert_url)

        # Click on JS alert button.
        page.once("dialog", lambda dialog: dialog.accept() if "I am a JS Alert" in dialog.message else None)
        page.get_by_text('Click for JS Alert').click()
        expect(page.locator('#result')).to_have_text("You successfully clicked an alert")

        # Click on JS confirm button.
        page.once("dialog", lambda dialog: dialog.accept() if "I am a JS Confirm" in dialog.message else dialog.dismiss())
        page.get_by_text('Click for JS Confirm').click()
        expect(page.locator('#result')).to_have_text("You clicked: Ok")

        # Click on JS prompt button.
        # page.on will listen to all the dialog events and handle them based on the message content.
        # page.once will listen to the next dialog event and handle it based on the message content.
        # It will not listen to any subsequent dialog events.
        page.on("dialog", lambda dialog: dialog.accept("Shafeeque") if "I am a JS prompt" in dialog.message else dialog.dismiss())
        page.get_by_text('Click for JS Prompt').click()
        expect(page.locator('#result')).to_have_text("You entered: Shafeeque")
        page.wait_for_timeout(3000)
        page.get_by_text('Click for JS Prompt').click()
        page.wait_for_timeout(3000)

def alerts_handler(dialog):
    """Handle JavaScript dialog events and accept or dismiss them based on the message."""
    if "I am a JS Alert" in dialog.message:
        dialog.accept()
    elif "I am a JS Confirm" in dialog.message:
        dialog.accept()
    elif "I am a JS prompt" in dialog.message:
        dialog.accept("Shafeeque")
    else:
        dialog.dismiss()

@pytest.mark.jsalert
def test_jsalerts_consolidated(page: Page, jsalert_url):
        '''This test case demonstrates the handling of JavaScript alerts in Playwright.
        It navigates to a webpage with JavaScript alerts, interacts with the alerts, and verifies the results.'''

        page.goto(jsalert_url)
        page.on("dialog", alerts_handler)

        # Click on JS alert button.
        page.get_by_text('Click for JS Alert').click()
        expect(page.locator('#result')).to_have_text("You successfully clicked an alert")

        # Click on JS confirm button.
        page.get_by_text('Click for JS Confirm').click()
        expect(page.locator('#result')).to_have_text("You clicked: Ok")

        # Click on JS prompt button.
        # page.on will listen to all the dialog events and handle them based on the message content.
        # page.once will listen to the next dialog event and handle it based on the message content.
        # It will not listen to any subsequent dialog events.
        page.get_by_text('Click for JS Prompt').click()
        expect(page.locator('#result')).to_have_text("You entered: Shafeeque")
        page.wait_for_timeout(3000)
