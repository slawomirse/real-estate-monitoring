from airflow import DAG
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, expect
from airflow.operators.python_operator import PythonOperator
from bs4 import BeautifulSoup
import json
import re
import logging
import yaml
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()
import sys



def create_list_of_offert_v1(ul_element):
    soup = BeautifulSoup(ul_element, 'html.parser')
    list_items = soup.find_all('li')
    list_elements = []
    for item in list_items:
        #Search article element
        article = item.find('article')
        if article is not None:
            #Initialize empty dictionary
            offert_info = {}
            #Get div element in article
            # Get the section with the offert details
            section = article.find('section')
            item_div_elements = section.find_all('div', recursive=False)[1]
            offert_title = clear_white_characters(item_div_elements.select_one('div > a > p').text)
            location_information = clear_white_characters(item_div_elements.select_one('a > p').text)
            location_information = clear_white_characters(item_div_elements.select_one('div > div > p').text)
            price = clear_white_characters(item_div_elements.select_one('div:nth-of-type(1) > span').text)
            surface = clear_white_characters(item_div_elements.select_one('div > div > div > dl > dt:-soup-contains("Powierzchnia") + dd').text)
            rooms= clear_white_characters(item_div_elements.select_one('div > div > div > dl > dt:-soup-contains("Liczba pokoi") + dd').text)
            offert_info['offert_title'] = offert_title
            offert_info['location'] = location_information
            offert_info['price'] = price
            offert_info['surface'] = surface
            offert_info['rooms'] = rooms
            offert_info['ingested_at'] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
            if offert_info['price'] != 'Zapytaj o cenę':
                list_elements.append(offert_info)
    return list_elements

def create_list_of_offert_v2(ul_element):
    soup = BeautifulSoup(ul_element, 'html.parser')
    list_items = soup.find_all('li')
    list_elements = []
    for item in list_items:
        #Search article element
        article = item.find('article')
        if article is not None:
            #Initialize empty dictionary
            offert_info = {}
            #Get div element in article
            # Get the section with the offert details
            section = article.find('section')
            item_div_elements = section.find_all('div', recursive=False)[1]
            offert_title = item_div_elements.select_one('div > a > p').text
            location_information = item_div_elements.select_one('div:nth-of-type(2) > p').text
            # Locate reduntant span element
            reduntant_span = item_div_elements.select_one('div:nth-of-type(1) > span').find('span')
            reduntant_span.decompose()
            price = item_div_elements.select_one('div:nth-of-type(1) > span').text
            surface = item_div_elements.select_one('div:nth-of-type(3) > dl > dt:-soup-contains("Powierzchnia") + dd').text.strip()
            rooms= item_div_elements.select_one('div:nth-of-type(3) > dl > dt:-soup-contains("Liczba pokoi") + dd').text.strip()
            offert_info['offert_title'] = offert_title
            offert_info['location'] = location_information
            offert_info['price'] = price
            offert_info['surface'] = surface
            offert_info['rooms'] = rooms
            offert_info['ingested_at'] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
            list_elements.append(offert_info)
    return list_elements

def get_web_url(base_url):
    pass

def get_content(**kwargs):
    logging.info('Data scraping started!')
    with sync_playwright() as p:
        # Launch a browser
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto('https://www.otodom.pl')
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
            offert_list = []
            while len(offert_list) <= 1000:
                if pagination_page == 1:
                        ul_element = page.locator("span:has-text('Wszystkie ogłoszenia') + ul").inner_html()
                        list_elements = create_list_of_offert_v1(ul_element)
                        offert_list += list_elements
                        pagination_page += 1
                else:
                    #Click the next page
                    page.locator('li[title="Go to next Page"]').click()
                    ul_element = page.locator("span:has-text('Wszystkie ogłoszenia') + ul").inner_html()
                    list_elements = create_list_of_offert_v1(ul_element)
                    offert_list += list_elements
                    pagination_page += 1
        except Exception as err:
            browser.close()
            logging.error(f'Unknown error occur: {err}')
            raise
        browser.close()
    # kwargs['ti'].xcom_push(key='shared_data', value=offert_list)
    return offert_list


def write_data_to_json_format(**kwargs):
    offert_list = kwargs['ti'].xcom_pull(task_ids='collect_data', key='shared_data')
    logging.info('Writing data to file')
    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        filename = f'/opt/airflow/output_files/{current_timestamp}_output.json'
        # Push the filename to XCom
        kwargs['ti'].xcom_push(key='filename', value=filename)
        with open(filename, 'w') as file:
            file.write(json.dumps(offert_list, indent=4))
    except Exception as err:
        logging.warn(f'Error during writing to file occur: {err}')
    logging.info(f'New {len(offert_list)} offert added')
    logging.info('Scraping finished successfully!')

def connect_to_mongodb():
    # Load the configuration from the file
    config = load_config()

    # Extract the connection details from the configuration
    uri = config['uri']
    tls = config['tls']
    tlsCertificateKeyFile = config['tlsCertificateKeyFile']
    serverApiVersion = config['serverApiVersion']

    # Connect to MongoDB using the extracted details
    client = MongoClient(uri,
                         tls=tls,
                         tlsCertificateKeyFile=tlsCertificateKeyFile,
                         server_api=ServerApi(serverApiVersion))

    db = client[config['db']]
    collection = db[config['collection']]
    return collection

def load_config():
    # Load the configuration from the YAML file
    with open('/opt/airflow/config/mongodb_connection_config.yaml') as file:
        config = yaml.safe_load(file)
    return config

def read_json_from_file(filepath):
    with open(filepath) as file:
        data = json.load(file)
    return data

def save_data_to_mongodb(**kwargs):
    collection = connect_to_mongodb()
    filename = kwargs['ti'].xcom_pull(task_ids='save_data_to_json_format', key='filename')
    data = read_json_from_file(filename)
    collection.insert_many(data)

default_args = {
    'owner': 'slawomirse',
    'start_date': datetime(2023, 11, 11, 2),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'extract_data_from_otodom.pl_and_save_into_json_format',
    default_args=default_args,
    schedule_interval='0 0 10 * *',  # Run day 10th of the month
)


get_data = PythonOperator(
    task_id='collect_data',
    python_callable=get_content,
    dag=dag,
)

save_data = PythonOperator(
    task_id='save_data_to_json_format',
    python_callable=write_data_to_json_format,
    provide_context=True,
    dag=dag,
)

save_data_to_database = PythonOperator(
    task_id='save_data_to_mongodb',
    python_callable=save_data_to_mongodb,
    provide_context=True,
    dag=dag,
)

get_data >> save_data >> save_data_to_database
