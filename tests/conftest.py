import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright

@pytest.fixture
def is_valid_date():
    def _is_valid_date(date_string, format_string):
        try:
            datetime.strptime(date_string, format_string)
            return True
        except ValueError:
            return False
    return _is_valid_date

@pytest.fixture(scope="session")
def browser():
    # Initialize Playwright once per session
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    # Create a new browser page before each test
    page = browser.new_page()
    yield page
    page.close()