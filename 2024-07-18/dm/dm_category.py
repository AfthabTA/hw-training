import requests
import logging
import json
import time
from settings import BASE_URL,HEADERS,START_URL,CATEGORY_URLS,CATEGORY_404,CATEGORY_FAILED
from parsel import Selector
from pipeline import MongoConnection


class DmCategory:

    def __init__(self):
        self.url = BASE_URL
        self.page = 1
        self.flag = 0
        self.mongo_connection = MongoConnection()
        self.category_urls = self.mongo_connection.db[CATEGORY_URLS]
        self.url_404 = self.mongo_connection.db[CATEGORY_404]
        self.url_failed = self.mongo_connection.db[CATEGORY_FAILED] 

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        

    def url_request(self):

        url = self.url
        # time.sleep(2)
        response = requests.get(url,HEADERS)
        if response.status_code == 200:

            logging.info(f'requst successful: {url}')
            self.category_finder(response,url)

        elif response.status_code == 404:

            logging.warning(f'url not found :{url}')
            try:
                product_url = {'url': url, 'statuscode': response.status_code,}
                self.url_404.insert_one(product_url)
                logging.info(f'url inserted into 404 collection : {url}')
            except Exception as e:
                logging.warning(f'failed to insert url :{url} Exception :{e}')
                  

        else :
            print(self.flag)
            self.flag += 1
            if self.flag <= 10:
                logging.error(f'retrying url: {url}')
                self.url_request()  
            else :
                self.flag = 0 
                try:
                      product_url = {'url':url, 'status':'Failed'}
                      self.url_failed.insert_one(product_url)
                      logging.info(f"url inserted into Failed collection : {url}")
                except Exception as e:
                     logging.warning(f"Failed to insert url :{url} Exception :{e}")
                print(self.page)
                self.page += 1
                self.url = f"https://product-search.services.dmtech.com/hu/search/crawl?allCategories.id=010000&pageSize=10&sort=editorial_relevance&type=search-static&currentPage={self.page}"
                self.url_request()   

    def category_finder(self, response, url):

        logging.info("working")

if __name__ == "__main__":
        obj = DmCategory()
        obj.url_request()

https://product-search.services.dmtech.com/hu/search/static?allCategories.id=010000&pageSize=10&sort=editorial_relevance&type=search-static
    https://product-search.services.dmtech.com/hu/search/static?allCategories.id=010100&pageSize=60&sort=editorial_relevance&type=search-static
    https://product-search.services.dmtech.com/hu/search/static?allCategories.id=010300&pageSize=60&sort=editorial_relevance&type=search-static
https://product-search.services.dmtech.com/hu/search/static?allCategories.id=020000&pageSize=10&sort=editorial_relevance&type=search-static
https://product-search.services.dmtech.com/hu/search/crawl?allCategories.id=110000&pageSize=10&sort=editorial_relevance&type=search-static
https://product-search.services.dmtech.com/hu/search/static?allCategories.id=021400&pageSize=10&sort=editorial_relevance&type=search-static
https://product-search.services.dmtech.com/hu/search/static?allCategories.id=030000&pageSize=10&sort=editorial_relevance&type=search-static    
https://product-search.services.dmtech.com/hu/search/static?allCategories.id=040000&pageSize=10&sort=editorial_relevance&type=search-static    
https://product-search.services.dmtech.com/hu/search/static?allCategories.id=050000&pageSize=10&sort=editorial_relevance&type=search-static
https://product-search.services.dmtech.com/hu/search/static?allCategories.id=060000&pageSize=10&sort=editorial_relevance&type=search-static
https://product-search.services.dmtech.com/hu/search/static?allCategories.id=070000&pageSize=10&sort=editorial_relevance&type=search-static
