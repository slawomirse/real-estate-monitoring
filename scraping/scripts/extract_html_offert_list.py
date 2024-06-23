from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from scraping.selectors.main_page_selectors import WebSelector as MainPageSelector
from scraping.selectors.offert_list_page_selectors import WebSelector as OffertListPageSelector
import re

select_main = MainPageSelector()
select_offert = OffertListPageSelector()


class ListProducer:
    def __init__(self, playwright) -> None:
        self.browser = playwright.firefox.launch(headless=True)
        page = self.browser.new_page()
        self.page = page
        self._location = None
        self.base_url = None

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location_value: str):
        self._location = location_value
        
    def open_browser(self):
        self.page.goto(select_main.get_web_url())

    def accept_cookies(self):
        self.page.locator(select_main.get_submit_cookies()).click()
    
    def click_location_button(self):
        #Version1
        try:
            self.page.locator(select_main.get_location_button()).click(timeout=3000)
            return 
        except PlaywrightTimeoutError:
            pass
        #Version2
        try:
            self.page.get_by_placeholder(select_main.get_location_placeholder()).click(timeout=3000)
        except PlaywrightTimeoutError:
            pass

    def type_location_information(self, location: str):
        self.location = location
        self.page.locator('input:not([readonly])[placeholder="Wpisz lokalizację"]').fill(self.location)

    def click_checkbox(self):
        #Version 1
        try:
            self.page.locator(select_main.get_checkbox_locator()).filter(has_text=re.compile(rf"{self.location},.*")).nth(0).get_by_role(select_main.get_checkbox_id()).click(timeout=3000)
            #Click in random place (price area)
            self.page.locator("#priceMin").click(timeout=3000)
            return
        except PlaywrightTimeoutError:
            pass
        #Version 2
        try:
            self.page.locator('div:text("Krakówmiasto, małopolskie")').click()
        except PlaywrightTimeoutError:
            pass


    def click_submit(self):
        submit_button = self.page.locator(select_main.get_submit_button())
        expect(submit_button).to_have_text(re.compile(rf"{select_main.get_submit_button_expected_pattern()}"), timeout=5000)
        submit_button.click()
        self.page.wait_for_url(re.compile(rf"{select_main.get_final_url_pattern()}"))

    def set_base_url(self):
        self.base_url =  self.page.url
    
    def get_paginated_url(self, page_number: int):
        return f"{self.base_url}?page={page_number}"
    
    def extract_list_of_html_offert(self, url: str):
        self.page.goto(url)
        return self.page.locator(select_offert.get_offert_list()).inner_html()
    
    def close_browser(self):
        self.browser.close()