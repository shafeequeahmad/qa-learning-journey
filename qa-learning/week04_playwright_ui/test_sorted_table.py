from playwright.sync_api import Page, expect
import pytest

# Tutorial: https://www.youtube.com/watch?v=n3qtOtrGw3Q&list=PLBw1ubD1J1UjtoSTM_4o1B9_QAjzXznrL&index=1

@pytest.mark.usefixtures("tables")
class BaseTest():
    pass

class TestSortedTable(BaseTest):

    @pytest.mark.stables
    def test_sorted_table(self, page: Page):
        '''This test case demonstrates the handling of sorted tables in Playwright.
        It navigates to a webpage with a sorted table, interacts with the table headers to sort
        the table, and verifies the results.'''

        page.goto(self.url)
        table = page.locator("table").nth(1)
        tr = table.locator("tr")
        expect(tr.first).to_be_visible()
        row_count = tr.count()
        print(f"Number of rows: {row_count}")


        population = []
        for i in range(1, row_count, 1):
            td = tr.nth(i).locator("td")
            if i == 0:
                td.nth(2).click()
                page.wait_for_timeout(3000)
                continue

            population.append(td.nth(2).inner_text().replace(",", ""))

        print("Polpulation:", population)


