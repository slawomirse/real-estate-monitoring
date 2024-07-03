import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from libraries.scraping.scripts.extract_html_offert_list import ListProducer


@pytest.fixture(scope="session")
def list_producer():
    with sync_playwright() as playwright:
        producer = ListProducer(playwright)
        yield producer  # Test runs here
        producer.close_browser()
