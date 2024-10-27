from libraries.scraping.scripts.extract_html_offert_list import ListProducer
from libraries.scraping.scripts.convert_html_list_to_list_of_dict import (
    HtmlToListOfDictConverter,
)
from playwright.sync_api import sync_playwright
import pytest


testing_data = [
    {"location": "Kraków", "number_of_offerts": 250},
    {"location": "Warszawa", "number_of_offerts": 100},
    {"location": "Wrocław", "number_of_offerts": 100},
]


def generate_offert_list(location: str, number_of_offerts: int):
    with sync_playwright() as playwright:
        try:
            playwright = ListProducer(playwright, location=location)
            playwright.open_browser()
            playwright.accept_cookies()
            playwright.click_location_button()
            playwright.type_location_information()
            playwright.click_checkbox()
            playwright.click_submit()
            playwright.set_base_url()
            pagination_page = 1
            city_based_list_paginated = []
            while len(city_based_list_paginated) < number_of_offerts:
                if pagination_page == 1:
                    url = playwright.base_url
                url = playwright.get_paginated_url(page_number=pagination_page)
                html_list = playwright.extract_list_of_html_offert(url=url)
                htlodc = HtmlToListOfDictConverter(
                    html_list=html_list, location=location
                )
                city_based_list = htlodc.create_list_of_offert()
                city_based_list_paginated += city_based_list
                if len(city_based_list_paginated) >= number_of_offerts:
                    city_based_list_paginated = city_based_list_paginated[
                        :number_of_offerts
                    ]
                pagination_page += 1
            return city_based_list_paginated
        except Exception as e:
            raise e
        finally:
            playwright.close_browser()


@pytest.mark.parametrize(
    "location, number_of_offerts",
    [(data["location"], data["number_of_offerts"]) for data in testing_data],
)
def test_end_to_end_scraping_process(location, number_of_offerts):
    offert_list = generate_offert_list(location, number_of_offerts)
    assert len(offert_list) == number_of_offerts
    assert isinstance(offert_list, list)
    assert isinstance(offert_list[0], dict)
    # Check duplicates
    unique_items = {tuple(sorted(d.items())) for d in offert_list}
    assert len(offert_list) == len(
        unique_items
    ), "There are duplicates in the offert list"
    assert (
        offert_list[0]["offert_title"] != offert_list[0]["location"]
    ), "Location should be different than title"
