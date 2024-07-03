from airflow.operators.python_operator import PythonOperator
from airflow import DAG

from libraries.scraping.scripts.extract_html_offert_list import ListProducer
from libraries.scraping.scripts.convert_html_list_to_list_of_dict import (
    HtmlToListOfDictConverter,
)
from libraries.database_connection.mongodb_connection import MongoDBConnection
from libraries.utilities.utils import read_json_from_file

from playwright.sync_api import sync_playwright

from datetime import datetime, timedelta
import json
import logging

from dotenv import load_dotenv

load_dotenv()


def generate_offert_list(location, number_of_offerts, **kwargs):
    logging.info("Data scraping started!")
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
                    city_based_list_paginated = city_based_list_paginated[
                        :number_of_offerts
                    ]
                pagination_page += 1
            kwargs["ti"].xcom_push(key="shared_data", value=city_based_list_paginated)
            return city_based_list_paginated
        except Exception as e:
            raise e
        finally:
            playwright.close_browser()


def write_data_to_json_format(**kwargs):
    offert_list = kwargs["ti"].xcom_pull(task_ids="collect_data", key="shared_data")
    logging.info("Writing data to file")
    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        filename = f"/opt/airflow/output_files/{current_timestamp}_output.json"
        # Push the filename to XCom
        kwargs["ti"].xcom_push(key="filename", value=filename)
        with open(filename, "w") as file:
            file.write(json.dumps(offert_list, indent=4))
    except Exception as err:
        logging.warn(f"Error during writing to file occur: {err}")
    logging.info(f"New {len(offert_list)} offert added")
    logging.info("Scraping finished successfully!")


def save_data_to_mongodb(**kwargs):
    mongo_instance = MongoDBConnection()
    mongo_instance.setup_connestion()
    filename = kwargs["ti"].xcom_pull(
        task_ids="save_data_to_json_format", key="filename"
    )
    data = read_json_from_file(filename)
    mongo_instance.conn.insert_many(data)
    mongo_instance.close_connection()


default_args = {
    "owner": "slawomirse",
    "start_date": datetime(2024, 7, 3),
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "extract_data_from_otodom.pl_and_save_into_json_format",
    default_args=default_args,
    schedule_interval="0 0 10 * *",  # Run day 10th of the month
)

get_data = PythonOperator(
    task_id="collect_data",
    python_callable=generate_offert_list,
    op_kwargs={"location": "Kraków", "number_of_offerts": 100},
    dag=dag,
)

save_data = PythonOperator(
    task_id="save_data_to_json_format",
    python_callable=write_data_to_json_format,
    provide_context=True,
    dag=dag,
)

save_data_to_database = PythonOperator(
    task_id="save_data_to_mongodb",
    python_callable=save_data_to_mongodb,
    provide_context=True,
    dag=dag,
)

get_data >> save_data >> save_data_to_database
