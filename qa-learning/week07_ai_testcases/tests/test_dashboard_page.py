import pytest
from pages.dashboard_page import DashboardPage
from constants.app_constants import BASE_URL

@pytest.mark.Smoke
def test_dashboard_login_and_url_validation(browser):
    """Validate opening login page, submitting credentials, and landing on Dashboard URL"""
    page = browser.new_page()
    dashboard_page = DashboardPage(page)
    
    # Validate exact landing URL
    assert page.url == BASE_URL + "/dashboard/index"

@pytest.mark.Sanity
def test_dashboard_header_elements(browser):
    """Validate presence of header logo and user profile dropdown"""
    page = browser.new_page()
    dashboard_page = DashboardPage(page)
    
    assert dashboard_page.is_brand_logo_visible(), "Brand Logo is not visible"
    assert dashboard_page.is_user_dropdown_visible(), "User Profile Dropdown is not visible"

@pytest.mark.Regression
def test_dashboard_side_menu_items(browser):
    """Validate presence and correct texts of all 12 side menu items"""
    page = browser.new_page()
    dashboard_page = DashboardPage(page)
    
    expected_menu_items = [
        "Admin", "PIM", "Leave", "Time", "Recruitment", "My Info",
        "Performance", "Dashboard", "Directory", "Maintenance", "Claim", "Buzz"
    ]
    
    actual_menu_items = dashboard_page.get_all_side_menu_texts()
    print(f"Actual Menu Items: {actual_menu_items}")
    
    for item in expected_menu_items:
        assert item in actual_menu_items, f"Side Menu Item '{item}' is missing from the sidebar"

@pytest.mark.Regression
def test_dashboard_widgets(browser):
    """Validate presence and correct titles of all 7 dashboard cards/widgets"""
    page = browser.new_page()
    dashboard_page = DashboardPage(page)
    
    expected_widgets = [
        "Time at Work", "My Actions", "Quick Launch", "Buzz Latest Posts",
        "Employees on Leave Today", "Employee Distribution by Sub Unit", "Employee Distribution by Location"
    ]
    
    actual_widgets = dashboard_page.get_all_widget_names()
    print(f"Actual Widgets: {actual_widgets}")
    
    for widget in expected_widgets:
        assert widget in actual_widgets, f"Dashboard Widget '{widget}' is missing from the dashboard page"

