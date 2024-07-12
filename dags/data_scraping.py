from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from airflow.utils.task_group import TaskGroup

from libraries.scraping.scripts.extract_html_offert_list import ListProducer
from libraries.scraping.scripts.convert_html_list_to_list_of_dict import (
    HtmlToListOfDictConverter,
)
from libraries.database_connection.mongodb_connection import MongoDBConnection
from libraries.utilities.utils import read_json_from_directory
from libraries.etl.etl_actions import ETLOperations

from playwright.sync_api import sync_playwright

from datetime import datetime, timedelta
import json
import logging
import os

from dotenv import load_dotenv

load_dotenv()


def generate_offert_list(location, number_of_offerts, **kwargs):
    logging.info("Data scraping started!")
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
                    pagination_page += 1
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
            kwargs["ti"].xcom_push(key=f"shared_data", value=city_based_list_paginated)
            kwargs["ti"].xcom_push(key=f"location", value=location)
            return city_based_list_paginated
        except Exception as e:
            raise e
        finally:
            playwright.close_browser()


def write_data_to_json_format(task_group_id, **kwargs):
    offert_list = kwargs["ti"].xcom_pull(
        task_ids=f"{task_group_id}.collect_data", key="shared_data"
    )
    location = kwargs["ti"].xcom_pull(
        task_ids=f"{task_group_id}.collect_data", key="location"
    )
    logging.info("Writing data to file")
    current_date = datetime.now().strftime("%Y-%m-%d")
    try:
        directory_path = f"/opt/airflow/output_files/{current_date}"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logging.info(f"Directory {directory_path} created")
        filename = os.path.join(directory_path, f"{location}.json")
        # Push the filename to XCom
        kwargs["ti"].xcom_push(key="directory_path", value=directory_path)
        with open(filename, "w") as file:
            file.write(json.dumps(offert_list, indent=4))
    except Exception as err:
        logging.warn(f"Error during writing to file occur: {err}")
    logging.info(f"New {len(offert_list)} offert added")
    logging.info("Scraping finished successfully!")


def save_data_to_mongodb(task_group_id, **kwargs):
    mongo_instance = MongoDBConnection()
    mongo_instance.setup_connestion()
    etl = ETLOperations(mongo_instance.conn)
    etl.clean_up_collection()
    directory_path = kwargs["ti"].xcom_pull(
        task_ids=f"{task_group_id}.save_data_to_json_format", key="directory_path"
    )
    logging.info(f"Reading data from {directory_path}")
    data = read_json_from_directory(directory_path)
    logging.info(f"Data sample: {data[:5]}")
    mongo_instance.conn.insert_many(data)
    mongo_instance.close_connection()


def transform_raw_data():
    # Read data from MongoDB
    mongo_instance = MongoDBConnection()
    mongo_instance.setup_connestion()
    etl = ETLOperations(mongo_instance.conn)
    data = etl.read_data()
    mongo_instance.close_connection()

    # Transform data
    mongo_instance = MongoDBConnection(
        path="config/transformations/mongodb_connection_config.yaml"
    )
    mongo_instance.setup_connestion()
    etl = ETLOperations(mongo_instance.conn)
    data = etl.transform_raw_data(data)
    etl.clean_up_collection()
    etl.save_data(data)
    mongo_instance.close_connection()


def load_data_to_datamart():
    mongo_instance = MongoDBConnection(
        path="config/transformations/mongodb_connection_config.yaml"
    )
    mongo_instance.setup_connestion()
    etl = ETLOperations(mongo_instance.conn)
    data = etl.read_data()
    mongo_instance.close_connection()

    mongo_instance = MongoDBConnection(
        path="config/datamart/mongodb_connection_config_write.yaml"
    )
    mongo_instance.setup_connestion()
    etl = ETLOperations(mongo_instance.conn)
    etl.save_data(data)
    mongo_instance.close_connection()


default_args = {
    "owner": "slawomirse",
    "start_date": datetime(2024, 7, 3),
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}


scraping_details = [
    {"location": "Kraków", "number_of_offerts": 500},
    {"location": "Warszawa", "number_of_offerts": 500},
    {"location": "Wrocław", "number_of_offerts": 500},
    {"location": "Białystok", "number_of_offerts": 250},
    {"location": "Bydgoszcz", "number_of_offerts": 250},
    {"location": "Gdańsk", "number_of_offerts": 250},
    {"location": "Katowice", "number_of_offerts": 250},
    {"location": "Kielce", "number_of_offerts": 250},
    {"location": "Lublin", "number_of_offerts": 250},
    {"location": "Łódź", "number_of_offerts": 250},
    {"location": "Olsztyn", "number_of_offerts": 250},
    {"location": "Opole", "number_of_offerts": 250},
    {"location": "Poznań", "number_of_offerts": 250},
    {"location": "Rzeszów", "number_of_offerts": 250},
    {"location": "Szczecin", "number_of_offerts": 250},
    {"location": "Toruń", "number_of_offerts": 250},
    {"location": "Zielona Góra", "number_of_offerts": 250},
]

with DAG(
    "extract_data_from_otodom.pl_and_save_into_json_format",
    default_args=default_args,
    schedule_interval="0 2 10 * *",  # Run at 2AM on the 10th of every month
) as dag:

    for scraping_detail in scraping_details:
        task_group_id = f"scrape_and_save_data_{scraping_detail['location']}"
        with TaskGroup(group_id=task_group_id) as scrape_and_save_data:
            get_data = PythonOperator(
                task_id="collect_data",
                python_callable=generate_offert_list,
                op_kwargs={
                    "location": scraping_detail["location"],
                    "number_of_offerts": scraping_detail["number_of_offerts"],
                },
            )

            save_data = PythonOperator(
                task_id=f"save_data_to_json_format",
                python_callable=write_data_to_json_format,
                op_kwargs={"task_group_id": task_group_id},
                provide_context=True,
            )
            get_data >> save_data

    save_data_to_database = PythonOperator(
        task_id="save_data_to_mongodb",
        python_callable=save_data_to_mongodb,
        op_kwargs={
            "task_group_id": f'scrape_and_save_data_{scraping_details[0]["location"]}'
        },
        provide_context=True,
    )

    transform_data = PythonOperator(
        task_id="transform_raw_data",
        python_callable=transform_raw_data,
        provide_context=True,
    )

    load_data_to_report_layer = PythonOperator(
        task_id="load_data_to_datamart",
        python_callable=load_data_to_datamart,
        provide_context=True,
    )

    (
        scrape_and_save_data
        >> save_data_to_database
        >> transform_data
        >> load_data_to_report_layer
    )
