from libraries.database_connection.mongodb_connection import MongoDBConnection
import pandas as pd


class ETLOperations:
    def __init__(self, conn: MongoDBConnection):
        self.conn = conn

    def read_data(self):
        return pd.DataFrame(self.conn.find())

    def clean_up_collection(self):
        self.conn.delete_many({})

    def transform_raw_data(self, data: pd.DataFrame):
        # Extract surface number from the surface column
        data["surface_number"] = data["surface"].str.split(" ").str[0].astype(float)
        data["formatted_date"] = pd.to_datetime(data["ingested_at"]).dt.strftime(
            "%Y-%m"
        )
        data["cleaned_price"] = (
            data["price"]
            .str.replace("zł", "")
            .str.replace(" ", "")
            .str.replace(",", ".")
            .astype(float)
            .round()
            .astype(int)
        )
        data["price_per_m2"] = (
            (data["cleaned_price"] / data["surface_number"]).round().astype(int)
        )
        data["rooms"] = self.standardize_room_column(data)
        return data

    def save_data(self, data: pd.DataFrame):
        self.conn.insert_many(data.to_dict(orient="records"))

    def standardize_room_column(self, data: pd.DataFrame):
        rooms_mapping = {
            "1 pokój": "1 room",
            "2 pokoje": "2 rooms",
            "3 pokoje": "3 rooms",
            "4 pokoje": "4 rooms",
            "5 pokoi": "5 rooms",
            "6 pokoi": "6 rooms",
            "7 pokoi": "7 rooms",
            "8 pokoi": "8 rooms",
            "9 pokoi": "9 rooms",
            "10 pokoi": "10 rooms",
        }
        return data["rooms"].map(rooms_mapping)
