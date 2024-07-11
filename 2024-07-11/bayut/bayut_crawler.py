from settings import base_url,headers,start_url
from pipeline import MongoConnection
from parsel import Selector
import requests
import json
import logging

class Bayut:

    def __init__ (self):

        self.headers = headers
        self.url_list = [] 
        self.page = 1
        self.url = start_url+'sale/'
        self.mongo_connection = MongoConnection()
        self.url_collection =  self.mongo_connection.db["bayut_product_urls"]
        self.error_collection = self.mongo_connection.db["bayut_request_error_url"]

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def request(self):

        self.page += 1
        print(self.url)
        response = requests.get(self.url, self.headers )
        
        if response.status_code == 200:

            html_data = response.text
            data_selector = Selector(html_data)
            url_list = data_selector.xpath('//li[@aria-label="Listing"]/article/div/a/@href').getall()
            next_url = data_selector.xpath('//a[@title="Next"]/@href').get()

            
            for url in url_list: 

                if url in self.url_list:
                     
                    logging.warning(f"url already inlist: {url}")        
                    continue
                
                
                property_url = 'https://www.bayut.eg'+url
                product_url = {'url': property_url,}

                try:
                    self.url_collection.insert_one(product_url)
                    logging.info(f"inserted property url: {property_url}") 
                except Exception as e:
                    logging.info(f"exception occured :{e} url :{property_url}")      
                self.url_list.append(url) 
            logging.info(f"success: {self.page}")
        
        else :
            
            logging.warning(f"url not found: {response.status_code}")
            try:
                self.error_collection.insert_one({'url': self.url, 'status_code': 404})
                logging.info(f"Inserted Error URL: {self.url}")
            except Exception as e:
                logging.warning(f"Error URL already exists: {self.url}")


        if self.page <= 200:
            
            if next_url is not None:

                self.url = 'https://www.bayut.eg'+next_url
                crawler.request()

            elif "rent/" not in self.url:

                self.url = start_url+'rent/' 
                self.page = 1  
                crawler.request()

            else : 

                logging.info("End of pages")                    
        else :

            if "rent/" not in self.url:
             
                self.url = start_url+'rent/' 
                self.page = 1  
                crawler.request()
                      
            
        file_name = "url_lidt.json"
        with open(file_name, 'w') as json_file:
            json.dump(self.url_list, json_file, indent = 4) 

if __name__ == "__main__":
    
    crawler = Bayut()
    crawler.request()
