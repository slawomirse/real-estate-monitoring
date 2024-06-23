from scraping.scripts.extract_html_offert_list import ListProducer
from scraping.scripts.convert_html_list_to_list_of_dict import HtmlToListOfDictConverter
from playwright.sync_api import sync_playwright

def generate_offert_list(location: str, number_of_offerts: int):
    with sync_playwright() as playwright:
        try:
            playwright = ListProducer(playwright)
            playwright.open_browser()
            playwright.accept_cookies()
            playwright.click_location_button()
            playwright.type_location_information(location=location)
            playwright.click_checkbox()
            playwright.click_submit()
            playwright.set_base_url()
            pagination_page = 1
            city_based_list_paginated = []
            while len(city_based_list_paginated) < number_of_offerts:
                if pagination_page == 1:
                    url = playwright.base_url
                    pagination_page += 1
                url = playwright.get_paginated_url(page_number=pagination_page)
                html_list = playwright.extract_list_of_html_offert(url=url)
                htlodc = HtmlToListOfDictConverter(html_list=html_list)
                city_based_list = htlodc.create_list_of_offert()
                city_based_list_paginated += city_based_list
                if len(city_based_list_paginated) >= number_of_offerts:
                    city_based_list_paginated = city_based_list_paginated[:number_of_offerts]
                pagination_page += 1
            return city_based_list_paginated
        except Exception as e:
            raise e
        finally:
            playwright.close_browser()
       
if __name__ == '__main__':
    offert_list = generate_offert_list(location='Kraków', number_of_offerts = 40)
    print(offert_list)