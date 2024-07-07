from pymongo import MongoClient
from pymongo.server_api import ServerApi
from libraries.utilities.utils import load_config
import logging


class MongoDBConnection:
    def __init__(self, path: str = "config/raw/mongodb_connection_config.yaml"):
        """
        Initialize MongoDB connection.
        :param config_path: MongoDB configuration detauls
        """
        self.conn = None
        self.client = None
        self.config_path = path

    def setup_connestion(self):
        """
        Setup MongoDB connection.
        """
        config = load_config(self.config_path)
        uri = config["uri"]
        tls = config["tls"]
        tlsCertificateKeyFile = config["tlsCertificateKeyFile"]
        serverApiVersion = config["serverApiVersion"]
        db = config["db"]
        collection = config["collection"]

        self.client = MongoClient(
            uri,
            tls,
            tlsCertificateKeyFile=tlsCertificateKeyFile,
            server_api=ServerApi(serverApiVersion),
        )
        db = self.client[db]
        self.conn = db[collection]
        logging.info("Connected to MongoDB successfully!")

    def close_connection(self):
        """
        Close MongoDB connection.
        """
        if self.client:
            self.client.close()
            self.conn = None
            logging.info("Connection closed successfully!")
