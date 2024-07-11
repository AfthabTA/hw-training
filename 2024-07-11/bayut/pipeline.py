from pymongo import MongoClient
import logging

uri = "mongodb://localhost:27017/"
db_name = "bayut_2024_07_09"  

class MongoConnection:
    
    def __init__(self):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        try:
            self.db["bayut_product_urls"].create_index("url", unique=True)
            self.db["bayut_product_data"].create_index("url", unique=True)
        except Exception as e:
            logging.warning(e)