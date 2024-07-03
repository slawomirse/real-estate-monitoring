from libraries.database_connection.mongodb_connection import MongoDBConnection
import pytest


def test_mongodb_connection():
    mongo_instance = MongoDBConnection()
    mongo_instance.setup_connestion()
    assert type(mongo_instance.conn.count_documents({})) == int
    mongo_instance.close_connection()

    # Assert that AttributeError is raised after the connection is closed
    with pytest.raises(AttributeError):
        _ = mongo_instance.conn.count_documents({})
