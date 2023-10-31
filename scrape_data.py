from playwright.sync_api import sync_playwright, expect
from bs4 import BeautifulSoup
import json
import re
import logging

logging.basicConfig(
    # format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p',
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    level=logging.DEBUG,
    filename='data_gathering.log',
    filemode='a'
)


class RealEstateDataProducer:

    def __init__(self, webpage, min_offert, headless=True):
        self.offert_list = []
        self.webpage = webpage
        self.headless = headless
        self.min_offert = min_offert

    def create_list_of_offert(self, ul_element):
        soup = BeautifulSoup(ul_element, 'html.parser')
        list_items = soup.find_all('li')
        for item in list_items:
            #Search article element
            article = item.find('article')
            if article is not None:
                #Initialize empty dictionary
                offert_info = {}
                #Get div element in article
                item_div_elements = article.find_all('div', recursive=False)
                location_information = article.find('p', recursive=False).text
                offert_title_div = item_div_elements[0]
                offert_title = offert_title_div.find('span').text
                offert_details = item_div_elements[1].find_all('span', recursive=False)
                price = offert_details[0].text
                surface = offert_details[3].text
                rooms = offert_details[2].text
                offert_info['offert_title'] = offert_title
                offert_info['location'] = location_information
                offert_info['price'] = price
                offert_info['surface'] = surface
                offert_info['rooms'] = rooms
                self.offert_list.append(offert_info)
        return self.offert_list


    def get_content(self):
        with sync_playwright() as p:
            # Launch a browser and create a context with cookie-related permissions disabled
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.webpage)
                # Wait for cookies pop-up and then accept
                page.locator('#onetrust-accept-btn-handler').click()
                #Click location button
                page.locator('button#location').click()
                #Populate with data
                page.locator('#location-picker-input').fill('Kraków')
                #Select proper checkbox
                page.locator("li").filter(has_text="Kraków, małopolskiemiasto").get_by_test_id("checkbox").click()
                # search when all parameters will apply properly
                submit_button = page.locator('#search-form-submit')
                expect(submit_button).to_have_text(re.compile(r"\w+ [0-9]+"))
                #Click search button
                submit_button.click()
                #Initialize 1st page of pagination
                pagination_page = 1
                #Wait for offert selector
                while len(self.offert_list) <= self.min_offert:
                    if pagination_page == 1:
                        ul_element = page.locator("span:has-text('Wszystkie ogłoszenia') + ul").inner_html()
                        self.create_list_of_offert(ul_element)
                        pagination_page += 1
                    else:
                        #Click the next page
                        page.locator('[data-cy="pagination.next-page"]').click()
                        ul_element = page.locator("span:has-text('Wszystkie ogłoszenia') + ul").inner_html()
                        self.create_list_of_offert(ul_element)
                        pagination_page += 1
            except Exception as err:
                browser.close()
                logging.error(f'Unknown error occur: {err}')
                raise
            
    def write_data_to_json_format(self):
        logging.info('Writing data to file')
        with open('output_json.json', 'w') as file:
            file.write(json.dumps(self.offert_list, indent=4))
        logging.info(f'New {len(self.offert_list)} offert added')

if __name__ == '__main__':
    scraping_object = RealEstateDataProducer(webpage='https://www.otodom.pl', min_offert=1000)
    logging.info('Data scraping started!')
    scraping_object.get_content()
    scraping_object.write_data_to_json_format()
    logging.info('Scraping finished successfully!')