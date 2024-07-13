from libraries.etl.etl_actions import ETLOperations
from libraries.database_connection.mongodb_connection import MongoDBConnection
import pandas as pd
from tabulate import tabulate


def test_transformation():
    mongo_instance = MongoDBConnection()
    mongo_instance.setup_connestion()
    db_op_instance = ETLOperations(mongo_instance.conn)
    data = db_op_instance.read_data()
    mongo_instance.close_connection()
    assert isinstance(data, pd.DataFrame)
