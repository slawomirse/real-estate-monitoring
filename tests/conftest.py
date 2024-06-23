import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from scraping.scripts.extract_html_offert_list import ListProducer

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
def list_producer():
    with sync_playwright() as playwright:
        producer = ListProducer(playwright)
        yield producer  # Test runs here
        producer.close_browser()

@pytest.fixture(scope="function")
def page(browser):
    # Create a new browser page before each test
    page = browser.new_page()
    yield page
    page.close()