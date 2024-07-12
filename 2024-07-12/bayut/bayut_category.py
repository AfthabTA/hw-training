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
        self.url = base_url
        self.main_category = []
        self.sub_category = []

    def request(self):

        url = "https://www.bayut.eg/en/egypt/commercial-for-sale/"
        response = requests.get(url,headers)
        if response.status_code == 200:

            logging.info(f'requst successful: {url}')
   
            self.main_category_finder(response,url)
          
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

    def main_category_finder(self, response, url):

        logging.info('working')   
        if url not in self.main_category :  

            html_data = response.text    
            selector_obj = Selector(html_data)   
            main_category_1 = selector_obj.xpath('//a[@aria-label="Find button"]/@href').get()  
            self.url = "https://www.bayut.eg"+main_category_1 
            self.main_category.append(self.url)
            self.sub_category.append(self.url)
            logging.info(self.url)
            self.request()
            

        elif url in self.main_category :

            html_data = response.text    
            selector_obj = Selector(html_data)
            main_category_2 = selector_obj.xpath('//a[@title="Properties for rent in Egypt"]/@href').get()
            main_category_2 = "https://www.bayut.eg"+main_category_2
            self.main_category.append(main_category_2)
            logging.info(main_category_2)

            end_categories = selector_obj.xpath('//div[@aria-label="Recommended searches"]/div/div/a/@href').getall()
            logging.info(end_categories)

    def sub_category_finder(self):
        logging.info("working")


if __name__ == '__main__':

    category_obj = Category()
    category_obj.request()        

    # https://px.ads.linkedin.com/wa/