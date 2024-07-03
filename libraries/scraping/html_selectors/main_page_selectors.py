page_elements = {
    "web_url": "http://www.otodom.pl",
    "submit_cookies": "#onetrust-accept-btn-handler",
    "location_placeholder": "Wpisz lokalizację",
    "location_button": "button#location",
    "location_placeholder_filtered": 'input:not([readonly])[placeholder="Wpisz lokalizację"]',
    "checkbox_locator": "li",
    "checkbox_id": "checkbox",
    "checkbox_click_v1": "#priceMin",
    "checkbox_click_v2": 'div:text("Krakówmiasto, małopolskie")',
    "submit_button": "#search-form-submit",
    "submit_button_expected_pattern": "\w+ [0-9]+",
    "final_url_pattern": "https://www\.otodom\.pl/pl/wyniki/sprzedaz/mieszkanie/.*",
}


class WebSelector:
    def __init__(self) -> None:
        self.web_url = page_elements["web_url"]
        self.submit_cookies = page_elements["submit_cookies"]
        self.location_button = page_elements["location_button"]
        self.location_placeholder_filtered = page_elements[
            "location_placeholder_filtered"
        ]
        self.location_placeholder = page_elements["location_placeholder"]
        self.checkbox_locator = page_elements["checkbox_locator"]
        self.checkbox_id = page_elements["checkbox_id"]
        self.checkbox_click_v1 = page_elements["checkbox_click_v1"]
        self.checkbox_click_v2 = page_elements["checkbox_click_v2"]
        self.submit_button = page_elements["submit_button"]
        self.submit_button_expected_pattern = page_elements[
            "submit_button_expected_pattern"
        ]
        self.final_url_pattern = page_elements["final_url_pattern"]

    def get_web_url(self):
        return self.web_url

    def get_submit_cookies(self):
        return self.submit_cookies

    def get_location_placeholder(self):
        return self.location_placeholder

    def get_location_button(self):
        return self.location_button

    def get_location_placeholder_filtered(self):
        return self.location_placeholder_filtered

    def get_checkbox_locator(self):
        return self.checkbox_locator

    def get_checkbox_click_v1(self):
        return self.checkbox_click_v1

    def get_checkbox_click_v2(self):
        return self.checkbox_click_v2

    def get_checkbox_id(self):
        return self.checkbox_id

    def get_submit_button(self):
        return self.submit_button

    def get_submit_button_expected_pattern(self):
        return self.submit_button_expected_pattern

    def get_final_url_pattern(self):
        return self.final_url_pattern
