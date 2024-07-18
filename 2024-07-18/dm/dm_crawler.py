import requests
import logging
import json
import time
import random
from settings import BASE_URL,HEADERS,START_URL,CRAWLER_404,CRAWLER_FAILED,PRODUCT_URL,USER_AGENTS
from parsel import Selector
from pipeline import MongoConnection


class DmCrawler:

    def __init__(self):
        self.url = START_URL
        self.page = 1
        self.flag = 0
        self.mongo_connection = MongoConnection()
        self.category_urls = self.mongo_connection.db[PRODUCT_URL]
        self.url_404 = self.mongo_connection.db[CRAWLER_404]
        self.url_failed = self.mongo_connection.db[CRAWLER_FAILED]
        self.headers = HEADERS['user-agent'] = USER_AGENTS[0]

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        

    def url_request(self):

        url = self.url
        # time.sleep(2)
        response = requests.get(url, self.headers )
        if response.status_code == 200:

            logging.info(f'requst successful: {url}')
            self.url_response(response,url)

        elif response.status_code == 404:

            logging.warning(f'url not found :{url}')
            try:
                product_url = {'url': url, 'statuscode': response.status_code,}
                self.url_404.insert_one(product_url)
                logging.info(f'url inserted into 404 collection : {url}')
            except Exception as e:
                logging.warning(f'failed to insert url :{url} Exception :{e}')

        elif response.status_code == 429:

            use_agent()
            def use_agent():
                random_user_agent = random.choice(USER_AGENTS)
                user_agent = HEADERS.pop('user_agent')
                if random_user_agent != user_agent:
                    logging.warning(f'User_agent changed {random_user_agent}')
                    self.headers = HEADERS['user_agent'] = random_user_agent
                else :
                    use_agent()

                
                    

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

    def url_response(self, response, url):
               
        logging.info('Working')
        self.flag = 0
        json_data = json.loads(response.text)
        if json_data['products'] is not None:
            if "&currentPage" not in url:
                self.url = f"https://product-search.services.dmtech.com/hu/search/crawl?allCategories.id=010000&pageSize=10&sort=editorial_relevance&type=search-static&currentPage={self.page}"
                self.url_request()
            else:
                print(self.page)
                self.page += 1
                self.url = f"https://product-search.services.dmtech.com/hu/search/crawl?allCategories.id=010000&pageSize=10&sort=editorial_relevance&type=search-static&currentPage={self.page}"
                self.url_request()
        else:
            logging.info('End')
            
                         

if __name__ == "__main__":

    obj = DmCrawler()
    obj.url_request()     
# &currentPage=1    

    # html_data = response.text
    #         selector_obj = Selector(html_data)
    #         brand = selector_obj.xpath('//div[@data-dmid="richtext"]/ul/li/div/div/a/@href').get()
    #         print(brand)                 