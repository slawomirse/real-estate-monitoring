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

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()