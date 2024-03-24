page_elements = {
    'web_url': 'http://www.otodom.pl',
    'submit_cookies': '#onetrust-accept-btn-handler',
    'location_button': 'button#location',
    'location_picker_input': '#location-picker-input',
    'checkbox_locator': "li",
    'checkbox_text': "Kraków, małopolskiemiasto",
    'checkbox_id': "checkbox",
}

class WebSelector:
    def __init__(self) -> None:
        self.web_url = page_elements['web_url']
        self.submit_cookies = page_elements['submit_cookies']
        self.location_button = page_elements['location_button']
        self.location_picker_input = page_elements['location_picker_input']
        self.checkbox_locator = page_elements['checkbox_locator']
        self.checkbox_text = page_elements['checkbox_text']
        self.checkbox_id = page_elements['checkbox_id']

    def get_web_url(self):
        return self.web_url
    
    def get_submit_cookies(self):
        return self.submit_cookies
    
    def get_location_button(self):
        return self.location_button
    
    def get_location_picker_input(self):
        return self.location_picker_input

    def get_checkbox_locator(self):
        return self.checkbox_locator
    
    def get_checkbox_text(self):
        return self.checkbox_text
    
    def get_checkbox_id(self):
        return self.checkbox_id