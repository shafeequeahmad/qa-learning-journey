from playwright.sync_api import Page, expect
from . import constant as const
from . import page as pageObj
import pytest

@pytest.mark.mockdata
@pytest.mark.mock_response
def test_mock_api_response(page: Page, burl):
    """Test case for mock api response."""
    jsonData = { "name": "Loquat", "id": 100}
    pageObj.mock_api_respose(
        page=page,
        jsonData=jsonData,
        testapi=const.MOCK_URL)

    pageObj.navigate_to_homepage(page=page, url=burl)

    # Assert that the new fruit is visible
    expect(page.get_by_text("Loquat", exact=True)).to_be_visible()
