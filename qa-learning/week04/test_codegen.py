import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.codegen
def test_example(page: Page) -> None:
    page.goto("https://playwright.dev/")
    expect(page.get_by_role("heading", name="Playwright enables reliable")).to_be_visible()
    expect(page.get_by_role("link", name="Get started")).to_be_visible()
    page.get_by_role("link", name="Get started").click()
    page.get_by_role("heading", name="Installation").click()
    page.get_by_role("heading", name="IntroductionDirect link to").click()
    page.get_by_role("navigation", name="Main").click()
    page.get_by_role("link", name="How to install Playwright").click()
    page.get_by_text("When prompted, choose /").click()
    expect(page.get_by_role("article")).to_contain_text("npm")
    page.get_by_role("heading", name="Updating PlaywrightDirect").click()
    page.get_by_role("heading", name="Updating PlaywrightDirect").dblclick()
