from bs4 import BeautifulSoup
from datetime import datetime
from libraries.scraping.html_selectors.offert_list_page_selectors import (
    WebSelector as OffertListPageSelector,
)
from libraries.utilities.utils import clear_white_characters

select_offert = OffertListPageSelector()


class HtmlToListOfDictConverter:
    def __init__(self, html_list: str):
        self.html_list = html_list
        self.soup = self._get_soup_instance()

    def _get_soup_instance(self):
        return BeautifulSoup(self.html_list, "html.parser")

    def create_offert_dict(self, item_div_elements: BeautifulSoup):
        offert_info = {}
        try:
            price = clear_white_characters(
                item_div_elements.select_one(select_offert.get_price()).text
            )
            if price == "Zapytaj o cenę":
                return offert_info
            offert_title = clear_white_characters(
                item_div_elements.select_one(select_offert.get_offert_title()).text
            )
            location_information = clear_white_characters(
                item_div_elements.select_one(
                    select_offert.get_location_information()
                ).text
            )
            surface = clear_white_characters(
                item_div_elements.select_one(select_offert.get_surface())
                .find(
                    select_offert.get_surface_label(),
                    text=select_offert.get_surface_label_text(),
                )
                .find_next_sibling(select_offert.get_surface_value())
                .text
            )
            rooms = clear_white_characters(
                item_div_elements.select_one(select_offert.get_rooms())
                .find(
                    select_offert.get_rooms_label(),
                    text=select_offert.get_rooms_label_text(),
                )
                .find_next_sibling(select_offert.get_rooms_value())
                .text
            )
            offert_info["offert_title"] = offert_title
            offert_info["location"] = location_information
            offert_info["price"] = price
            offert_info["surface"] = surface
            offert_info["rooms"] = rooms
            offert_info["ingested_at"] = str(
                datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            )
            return offert_info
        except:
            return {}

    def create_list_of_offert(self):
        list_items = self.soup.find_all("li")
        list_elements = []
        for item in list_items:
            article = item.find("article")
            if article is not None:
                section = article.find("section")
                item_div_elements = section.find_all("div", recursive=False)[1]
                offert_info_dict = self.create_offert_dict(item_div_elements)
                if len(offert_info_dict) > 0:
                    list_elements.append(offert_info_dict)
        return list_elements
