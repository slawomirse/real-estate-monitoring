from dags.data_scraping import create_list_of_offert_v1 
import pytest
import os
from playwright.sync_api import expect
import re

def template_content():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates/html')
    template_files = os.listdir(template_dir)
    template_contents = {}
    for template_file in template_files:
        template_path = os.path.join(template_dir, template_file)
        with open(template_path, 'r') as file:
            template_content = file.read()
            template_contents[template_file] = template_content
    return template_contents

def test_get_page_title(page):
    page.goto('http://www.otodom.pl')
    expect(page.locator('#onetrust-accept-btn-handler')).to_be_visible()
    # page.locator('button#location').click()
    


# @pytest.mark.parametrize('file_name, params', template_content().items(), ids=[i for i in template_content().keys()])
# def test_create_list_of_offert_v1(file_name, params, is_valid_date):
#     print(f'File name: {file_name}')
#     output_dict = create_list_of_offert_v1(params)
#     assert isinstance(output_dict, list)
#     for offert in output_dict:
#         assert isinstance(offert, dict)
#         required_keys = ['offert_title', 'location', 'price', 'surface', 'rooms', 'ingested_at']
#         location_keys = ['ul.', 'os.', 'osiedle', 'al.', 'aleja', 'plac', 'rondo', 'Kraków', 'małopolskie']
#         assert all(key in offert for key in required_keys)
#         assert len(offert['offert_title']) > 0
#         assert any(key in offert['location'] for key in location_keys)
#         assert 'zł' in offert['price']
#         assert 'm²' in offert['surface']
#         assert 'pokój' or 'pokoje' in offert['rooms']
#         assert is_valid_date(offert['ingested_at'], "%Y-%m-%dT%H:%M:%S")
        