import logging
from pymongo import MongoClient
from settings import MONGO_URL,DB_NAME


class MongoConnection:
    
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[DB_NAME]
        try:
            self.db["bayut_product_urls"].create_index("url", unique=True)
            self.db["bayut_product_data"].create_index("url", unique=True)
        except Exception as e:
            logging.warning(e)