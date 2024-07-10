from settings import headers
from pipeline import MongoConnection
from parsel import Selector
import requests
import logging
import re

class BayutPasrser:

    def __init__(self):

        self.mongo_connection = MongoConnection()
        self.url_collection =  self.mongo_connection.db["bayut_product_urls"]
        self.data_collection = self.mongo_connection.db["bayut_product_data"]
        self.url_404 = self.mongo_connection.db["bayut_parser_404"]
        self.url_failed = self.mongo_connection.db["bayut_parser_failed"]
        self.flag = 0

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def url_parser(self):

        for item in self.url_collection.find():
            url = item.get('url', '')
            if url:
                data_url = self.data_collection.find_one({'url': url})
                if not data_url:    

                    self.url_request(url)

    def url_request(self,url):


        response = requests.get(url,headers)
        if response.status_code == 200:

            logging.info(f'requst successful: {url}')
            self.data_parser(response,url)

        elif response.status_code == 404:

            logging.warning(f'url not found :{url}')
            try:
                product_url = {'url': url, 'statuscode': response.status_code,}
                self.url_404.insert_one(product_url)
                logging.info(f'url inserted into 404 collection : {url}')
            except Exception as e:
                logging.warning(f'failed to insert url :{url} Exception :{e}')
                  

        else :

            self.flag += 1
            if self.flag <= 5:
                logging.error(f'retrying url: {url}')
                self.url_request(url)  
            else :
                self.flag = 0 
                try:
                      product_url = {'url':url, 'status':'Failed'}
                      self.url_failed.insert_one(product_url)
                      logging.info(f"url inserted into Failed collection : {url}")
                except Exception as e:
                     logging.warning(f"Failed to insert url :{url} Exception :{e}")
                               


    def data_parser(self,response,url):

            html_data = response.text
            selector_obj = Selector(html_data)
            pattern = "-(\d*)."

            ad_id = re.findall(pattern, url)    
            title = selector_obj.xpath('//h1/text()').get()
            breadcrumb1 =selector_obj.xpath('//div[@aria-label="Breadcrumb"]/div/text()').get()
            breadcrumb2 =selector_obj.xpath('//div[@aria-label="Breadcrumb"]/a/span/text()').getall()
            breadcrumb3 =selector_obj.xpath('//div[@aria-label="Breadcrumb"]/span/text()').get()
            price = selector_obj.xpath('//span[@aria-label="Price"]/text()').get()
            currency = selector_obj.xpath('//span[@aria-label="Currency"]/text()').get()
            image_url = selector_obj.xpath('//div[@aria-label="Property image"]/div/picture/source/@srcset').get()
            description = selector_obj.xpath('//div[@aria-label="Property description"]/div/span/text()').getall()
            seller_name = selector_obj.xpath('//span[@aria-label="Agency name"]/text()').get()
            location = selector_obj.xpath('//div[@aria-label="Property header"]/text()').get()
            property_type = selector_obj.xpath('//span[@aria-label="Type"]/text()').get()
            bathroom = selector_obj.xpath('//span[@aria-label="Baths"]/span/text()').get()
            bedroom = selector_obj.xpath('//span[@aria-label="Beds"]/span/text()').get()

            breadcrumb2.insert(0,breadcrumb1)
            breadcrumb2.append(breadcrumb3)
            price_dic = {"currency": currency,"price": price}
            
            if bathroom is not None:
                num_bathroom = bathroom[0]
                num_bathroom = int((num_bathroom))
            else :
                num_bathroom = 0

            if bedroom is not None:
                num_bedroom = bedroom[0]
                if num_bedroom.isdigit() == True:
                    num_bedroom = int(num_bedroom)
                else :
                    num_bedroom = bedroom 
            else :
                num_bedroom = 0        
                    
            ad_id = ad_id.pop()
            

            item = {
                    'url': url,
                    'property_name': title,
                    'property_id': ad_id,
                    'breadcrumbs': breadcrumb2,
                    'price': price_dic,
                    'image_url': image_url,
                    'description': description,
                    'seller_name': seller_name,
                    'location': location,
                    'property_type': property_type,
                    'bathrooms': num_bathroom,
                    'bedrooms': num_bedroom
                     
                        }
            
            logging.info(item)
            try:
                self.data_collection.insert_one(item)
                logging.info("item information saved successfully")
            except Exception as e:
                logging.error(f"failed to save information: {e}") 



if __name__ == "__main__":

    parser = BayutPasrser()
    parser.url_parser()              
