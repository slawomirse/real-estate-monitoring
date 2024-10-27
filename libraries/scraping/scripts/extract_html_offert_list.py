from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from libraries.scraping.html_selectors.main_page_selectors import (
    WebSelector as MainPageSelector,
)
from libraries.scraping.html_selectors.offert_list_page_selectors import (
    WebSelector as OffertListPageSelector,
)
import re

select_offert = OffertListPageSelector()


class ListProducer:
    """
    A class that represents a list producer for extracting HTML offers.

    Attributes:
        browser: The browser instance used for scraping.
        page: The page instance used for navigation.
        location: The location for which the offers are extracted.
        base_url: The base URL of the website.
        select_main: An instance of MainPageSelector for selecting elements on the main page.

    Methods:
        open_browser: Opens the browser and navigates to the main page.
        accept_cookies: Accepts the cookies on the main page.
        click_location_button: Clicks the location button on the main page.
        type_location_information: Types the location information on the main page.
        click_checkbox: Clicks the checkbox for the specified location on the main page.
        click_submit: Clicks the submit button on the main page.
        set_base_url: Sets the base URL of the website.
        get_paginated_url: Returns the URL for a specific page number.
        extract_list_of_html_offert: Extracts the list of HTML offers from a given URL.
        close_browser: Closes the browser.
    """

    def __init__(self, playwright, location) -> None:
        self.browser = playwright.firefox.launch(headless=True)
        page = self.browser.new_page()
        self.page = page
        self.location = location
        self.base_url = None
        self.select_main = MainPageSelector(location=location)

    def open_browser(self) -> None:
        self.page.goto(self.select_main.get_web_url())

    def accept_cookies(self) -> None:
        self.page.locator(self.select_main.get_submit_cookies()).click()

    def click_location_button(self) -> None:
        # Version1
        try:
            self.page.locator(self.select_main.get_location_button()).click(
                timeout=3000
            )
            return
        except PlaywrightTimeoutError:
            pass
        # Version2
        try:
            self.page.get_by_placeholder(
                self.select_main.get_location_placeholder()
            ).click(timeout=3000)
        except PlaywrightTimeoutError:
            pass

    def type_location_information(self) -> None:
        self.page.locator(self.select_main.get_location_placeholder_filtered()).fill(
            self.location
        )

    def click_checkbox(self) -> None:
        # Version 1
        try:
            self.page.locator(self.select_main.get_checkbox_locator()).filter(
                has_text=re.compile(rf"{self.location},.*")
            ).nth(0).get_by_role(self.select_main.get_checkbox_id()).click(timeout=3000)
            # Click in random place (price area)
            self.page.locator(self.select_main.get_checkbox_click_v1()).click(
                timeout=3000
            )
            return
        except PlaywrightTimeoutError:
            pass
        # Version 2
        try:
            self.page.locator(self.select_main.get_checkbox_click_v2()).click()
        except PlaywrightTimeoutError:
            pass

    def click_submit(self) -> None:
        submit_button = self.page.locator(self.select_main.get_submit_button())
        expect(submit_button).to_have_text(
            re.compile(rf"{self.select_main.get_submit_button_expected_pattern()}"),
            timeout=5000,
        )
        submit_button.click()
        self.page.wait_for_url(
            re.compile(rf"{self.select_main.get_final_url_pattern()}")
        )

    def set_base_url(self) -> None:
        self.base_url = self.page.url

    def get_paginated_url(self, page_number: int) -> str:
        return f"{self.base_url}?page={page_number}&page={page_number}"

    def extract_list_of_html_offert(self, url: str) -> str:
        self.page.goto(url)
        return self.page.locator(select_offert.get_offert_list()).inner_html()

    def close_browser(self) -> None:
        self.browser.close()
