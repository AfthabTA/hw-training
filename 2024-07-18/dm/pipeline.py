import logging
from pymongo import MongoClient
from settings import MONGO_URL,DB_NAME,PRODUCT_URL,PRODUCT_DATA


class MongoConnection:
    
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[DB_NAME]
        try:
            self.db[PRODUCT_URL].create_index("url", unique=True)
            self.db[PRODUCT_DATA].create_index("url", unique=True)
        except Exception as e:
            logging.warning(e)