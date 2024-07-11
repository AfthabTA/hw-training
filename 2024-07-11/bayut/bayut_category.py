from settings import base_url, headers, category_headers
from pipeline import MongoConnection
import requests
from parsel import Selector
import logging
import re
import json


class Category:

    def __init__(self):

        self.flag = 0
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    def request(self):

        url = base_url
        response = requests.get(url,headers)
        if response.status_code == 200:

            logging.info(f'requst successful: {url}')
            self.category_finder(response,url)

        elif response.status_code == 404:

            logging.warning(f'url not found :{url}')
            try:
                product_url = {'url': url, 'statuscode': response.status_code,}
                # self.url_404.insert_one(product_url)
                logging.info(f'url inserted into 404 collection : {url}')
            except Exception as e:
                logging.warning(f'failed to insert url :{url} Exception :{e}')

        else :

            self.flag += 1
            if self.flag <= 5:
                logging.error(f'retrying url: {url}')
                self.request(url)  
            else :
                self.flag = 0 
                try:
                      product_url = {'url':url, 'status':'Failed'}
                    #   self.url_failed.insert_one(product_url)
                      logging.info(f"url inserted into Failed collection : {url}")
                except Exception as e:
                     logging.warning(f"Failed to insert url :{url} Exception :{e}")        

    def category_finder(self, response, url):

        logging.info('working')     
        html_data = response.text    
        selector_obj = Selector(html_data)   
        main_category = selector_obj.xpath('//a[@aria-label="Find button"]/@href').get()   
        var = '/html/body/script[1]/text()'
        script_data = selector_obj.xpath(var).extract_first()
        # script_data = json.loads(script_data)
        print(main_category)

if __name__ == '__main__':

    category_obj = Category()
    category_obj.request()        

    # https://px.ads.linkedin.com/wa/