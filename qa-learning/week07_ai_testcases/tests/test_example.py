
import pytest
from pages.example_page import ExamplePage
from constants.app_constants import BASE_URL

@pytest.mark.Smoke
def test_verify_navigation_menu(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    example_page.verify_navigation_menu()

@pytest.mark.Smoke
def test_verify_breadcrumbs(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    example_page.verify_breadcrumbs()

@pytest.mark.Smoke
def test_verify_hyperlinks(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    example_page.verify_hyperlinks()

@pytest.mark.Sanity
def test_verify_username_field(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#txtUsername").is_visible()

@pytest.mark.Sanity
def test_verify_user_role_dropdown(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#user_role").is_visible()

@pytest.mark.Sanity
def test_verify_employee_name_field(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#employee_name").is_visible()

@pytest.mark.Sanity
def test_verify_status_dropdown(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#status").is_visible()

@pytest.mark.Sanity
def test_verify_search_button(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#searchBtn").is_visible()

@pytest.mark.Sanity
def test_verify_reset_button(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#resetBtn").is_visible()

@pytest.mark.Sanity
def test_verify_add_button(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#addBtn").is_visible()

@pytest.mark.Regression
def test_verify_table_data(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#table_data").is_visible()

@pytest.mark.Regression
def test_verify_table_headers(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#table_headers").is_visible()

@pytest.mark.Regression
def test_verify_records_found_text(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#records_found_text").is_visible()

@pytest.mark.Regression
def test_verify_actions_column(browser):
    page = browser.new_page()
    example_page = ExamplePage(page)
    example_page.login()
    page.goto(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")
    assert page.query_selector("#actions_column").is_visible()
