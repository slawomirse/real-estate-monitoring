from libraries.scraping.scripts.convert_html_list_to_list_of_dict import (
    HtmlToListOfDictConverter,
)
import pytest
import os
from datetime import datetime


def is_valid_date(date_string, format_string):
    try:
        datetime.strptime(date_string, format_string)
        return True
    except ValueError:
        return False


def template_content():
    template_dir = os.path.join(os.path.dirname(__file__), "../templates/html")
    template_files = os.listdir(template_dir)
    template_contents = {}
    for template_file in template_files:
        template_path = os.path.join(template_dir, template_file)
        with open(template_path, "r") as file:
            template_content = file.read()
            template_contents[template_file] = template_content
    return template_contents


@pytest.mark.parametrize(
    "file_name, html_content",
    template_content().items(),
    ids=[i for i in template_content().keys()],
)
def test_converting_html_to_dict(file_name, html_content):
    html_to_list_instance = HtmlToListOfDictConverter(html_list=html_content)
    output_dict = html_to_list_instance.create_list_of_offert()
    assert isinstance(output_dict, list)
    for offert in output_dict:
        assert isinstance(offert, dict)
        required_keys = [
            "offert_title",
            "location",
            "price",
            "surface",
            "rooms",
            "ingested_at",
        ]
        location_keys = [
            "ul.",
            "os.",
            "osiedle",
            "al.",
            "aleja",
            "plac",
            "rondo",
            "Kraków",
            "małopolskie",
        ]
        assert all(key in offert for key in required_keys)
        assert len(offert["offert_title"]) > 0
        assert any(key in offert["location"] for key in location_keys)
        assert "zł" in offert["price"]
        assert "m²" in offert["surface"]
        assert "pokój" or "pokoje" in offert["rooms"]
        assert is_valid_date(offert["ingested_at"], "%Y-%m-%dT%H:%M:%S")
