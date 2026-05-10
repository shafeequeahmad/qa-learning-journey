from . import page as pageobj
from . import constant as const
import pytest
from playwright.sync_api import Page, expect

class TestMockData():
    """Test class for API mock data validation."""

    @pytest.mark.mockdata
    @pytest.mark.mock_request
    def test_mock_data(self, burl, page: Page):
        '''
        This test is to check mocking behaviour.
        Here Strawberry1 is not present on URL but as we mocked it.
        Test will be pass response
        '''

        pageobj.mock_api_request(
            page = page,
            jsonData = [{"name": "Strawberry1", "id": 21}],
            testapi = const.MOCK_URL
        )

        pageobj.navigate_to_homepage(page=page, url=burl)
        expect(page.get_by_text("Strawberry1")).to_be_visible()






