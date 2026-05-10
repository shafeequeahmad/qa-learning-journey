from playwright.sync_api import Page, expect
import pytest

# Tutorial: https://www.youtube.com/watch?v=Juq23qJloZk&list=PLBw1ubD1J1UjtoSTM_4o1B9_QAjzXznrL&index=2

@pytest.mark.usefixtures("tables")
class BaseTest():
    """Base test class for Playwright or Selenium test suites."""
    pass

class TestTables(BaseTest):
    """Test class for table handling and validation."""

    @pytest.mark.tables
    def test_tables(self, page: Page):
        '''This test case demonstrates the handling of tables in Playwright.
        It navigates to a webpage with a table, interacts with the table elements, and verifies
        the results.'''

        page.goto(self.url)
        table = page.locator("//h4[@id='simple-table-item-prices']/../*/table")
        tr = table.locator("tr")
        row_count = tr.count()
        print(f"Number of rows: {row_count}")

        for i in range(row_count - 1):
            td = tr.nth(i+1).locator("td")
            cell_count = td.count()
            print(f"Row {i+1}", end=" ")
            for j in range(cell_count):
                cell_text = td.nth(j).inner_text()
                print(f"{cell_text}", end=" ")
            print()


