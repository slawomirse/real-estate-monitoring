def test_extracing_html_data(list_producer, location="Kraków"):
    playwright = list_producer
    playwright.open_browser()
    playwright.accept_cookies()
    playwright.click_location_button()
    playwright.type_location_information(location=location)
    playwright.click_checkbox()
    playwright.click_submit()
    playwright.set_base_url()
    assert "otodom" in playwright.base_url
