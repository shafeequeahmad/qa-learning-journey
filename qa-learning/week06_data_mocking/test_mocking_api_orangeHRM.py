from . import constant as const
from playwright.sync_api import Page, Route, expect
import pytest

@pytest.fixture
def login(page: Page):
    """Fixture to log in to the application for tests."""
    page.goto(const.ORANGE_HRM)
    page.fill('input[name="username"]', const.ORANGE_USER)
    page.fill('input[name="password"]', const.ORANGE_PASSWORD)
    page.click('button[type="submit"]')

    expect(page.locator('//p[text()="Time at Work"]')).to_be_visible()


def mockdata(page: Page, data):
    """Register a mock route for OrangeHRM dashboard action-summary responses."""
    def handle(route: Route):
        """Route handler that modifies the dashboard API response before fulfillment."""
        response = route.fetch()
        jsondata = response.json()

        print(f" ---> Original response: {jsondata}")  # Debug: see original data

        if isinstance(jsondata, dict):
            if 'data' in jsondata and isinstance(jsondata['data'], list):
                # jsondata['data'].append(data) >> website under test does not allow to add
                jsondata['data'][0]['pendingActionCount'] = 20
                jsondata['data'][1]['pendingActionCount'] = 200

        route.fulfill(json=jsondata)  # Just json, not response=json

    page.route(const.ORANGE_MOCK_URL, handle)


@pytest.mark.login
def test_orangeHRM(login, page: Page):
    """Test case for orangeHRM."""
    data = {
        "id": 50,
        "group": "Candidates To Interview Shafeeque",
        "pendingActionCount": 1
    }
    mockdata(page=page, data=data)
    page.reload()

    # Wait for page to load and check if mock worked
    page.wait_for_timeout(3000)

    # Check if the mocked data appears in the page content
    page_content = page.content()
    if "Candidates To Interview Shafeeque" in page_content:
        print("✅ Mock data found in page content!")
    else:
        print("❌ Mock data NOT found in page content")

    # Alternative: Check specific elements that might display this data
    # Look for elements containing the group name
    elements = page.locator('text=/Candidates To Interview/').all()
    if elements:
        print(f"✅ Found {len(elements)} elements with mock data text")
    else:
        print("❌ No elements found with mock data text")

    page.wait_for_timeout(7000)  # Remaining wait time

