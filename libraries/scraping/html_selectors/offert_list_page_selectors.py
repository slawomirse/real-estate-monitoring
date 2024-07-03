page_elements = {
    'offert_list': 'span:has-text("Wszystkie ogłoszenia") + ul',
    'offert_title': 'div > a > p',
    'price': 'div:nth-of-type(1) > span',
    'location_information': 'a > p',
    'surface': 'div:nth-of-type(3)',
    'surface_label': 'dt',
    'surface_value': 'dd',
    'surface_label_text': 'Powierzchnia',
    'rooms': 'div:nth-of-type(3)',
    'rooms_label': 'dt',
    'rooms_value': 'dd',
    'rooms_label_text': 'Liczba pokoi'
}

class WebSelector:
    def __init__(self) -> None:
        self.offert_list = page_elements['offert_list']
        self.offert_title = page_elements['offert_title']
        self.price = page_elements['price']
        self.location_information = page_elements['location_information']
        self.surface = page_elements['surface']
        self.surface_label = page_elements['surface_label']
        self.surface_label_text = page_elements['surface_label_text']
        self.surface_value = page_elements['surface_value']
        self.rooms = page_elements['rooms']
        self.rooms_label = page_elements['rooms_label']
        self.rooms_value = page_elements['rooms_value']
        self.rooms_label_text = page_elements['rooms_label_text']


    def get_offert_list(self):
        return self.offert_list
    
    def get_offert_title(self):
        return self.offert_title
    
    def get_price(self):
        return self.price
    
    def get_location_information(self):
        return self.location_information
    
    def get_surface(self):
        return self.surface
    
    def get_surface_label(self):
        return self.surface_label
    
    def get_surface_label_text(self):
        return self.surface_label_text
    
    def get_surface_value(self):
        return self.surface_value
    
    def get_rooms(self):
        return self.rooms
    
    def get_rooms_label(self):
        return self.rooms_label
    
    def get_rooms_value(self):
        return self.rooms_value
    
    def get_rooms_label_text(self):
        return self.rooms_label_text
    
    
    
