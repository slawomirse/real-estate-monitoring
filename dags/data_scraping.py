from airflow import DAG
from datetime import datetime
from RealEstateDataProducer import RealEstateDataProducer  # Import your Python class
from ExecutePythonClassMethod import ExecutePythonClassMethod  # Import your custom operator

default_args = {
    'owner': 'slawomirse',
    'start_date': datetime(2023, 11, 11),
}

dag = DAG(
    'extract_data_from_otodom.pl_and_save_into_json_format',
    default_args=default_args,
    schedule_interval='0 0 10 * *',  # Adjust the schedule interval as needed
)

my_class_instance = RealEstateDataProducer(webpage='https://www.otodom.pl', min_offert=1000)

task_method1 = ExecutePythonClassMethod(
    task_id='Collect_data',
    python_class=my_class_instance,
    method_name='get_content',  # Specify the method to execute
    dag=dag,
)

task_method2 = ExecutePythonClassMethod(
    task_id='Save_data_to_json_format',
    python_class=my_class_instance,
    method_name='write_data_to_json_format',  # Specify the method to execute
    dag=dag,
)

task_method1 >> task_method2