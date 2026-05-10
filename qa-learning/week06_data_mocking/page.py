from playwright.sync_api import Page, Route, expect
import pytest

def navigate_to_homepage(page: Page, url: str):
    """Navigate to the homepage URL and verify the page heading."""
    page.goto(url)
    expect(page.locator('h1.py-4')).to_have_text('Render a List of Fruits')

def mock_api_request(page: Page, jsonData, testapi):
    """Intercept the fruit API request and fulfill it with the provided mock JSON."""
    # page.route(testapi, lambda route: route.fulfill(
    #     json = jsonData
    # ))
    # another way of declaration is also correct, below is the another way
    def handle(route: Route):
        """Route handler that intercepts the network request and fulfills it with mocked JSON."""
        route.fulfill(
            json = jsonData
        )
    # Intercept the route to the fruit API
    page.route(testapi, handle)

def mock_api_respose(page: Page, jsonData, testapi):
    """Intercept the fruit API response, append mock data, and fulfill the route."""
    def handle(route: Route):
        """Route handler that intercepts network traffic and fulfills it with mocked JSON."""
        response = route.fetch()
        body = response.json()
        body.append(jsonData)
        # Fulfill using the original response, while patching the response body
        # with the given JSON object.
        route.fulfill(response=response, json=body)

    page.route(testapi, handle)





