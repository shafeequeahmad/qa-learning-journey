from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navigating to login page...")
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        page.wait_for_load_state("networkidle")
        
        print("Filling credentials...")
        page.fill("input[name='username']", "Admin")
        page.fill("input[name='password']", "admin123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        
        print(f"Logged in. Current URL: {page.url}")
        
        # Take a screenshot to verify it visually
        page.screenshot(path="dashboard_screenshot.png")
        print("Screenshot saved to dashboard_screenshot.png")
        
        # Get side panel menu texts
        print("\n--- Side Panel Menu ---")
        menu_items = page.query_selector_all(".oxd-main-menu-item")
        for item in menu_items:
            print(item.inner_text().strip())
            
        # Get dashboard widget headers
        print("\n--- Dashboard Widgets ---")
        widgets = page.query_selector_all(".orangehrm-dashboard-widget-name")
        for w in widgets:
            print(w.inner_text().strip())
            
        browser.close()

if __name__ == "__main__":
    inspect()
