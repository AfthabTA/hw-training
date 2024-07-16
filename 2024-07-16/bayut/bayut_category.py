
import logging
import json
import requests
from settings import BASE_URL, HEADERS, CATEGORY_URLS,CATEGORY_404,CATEGORY_FAILED
from pipeline import MongoConnection
from parsel import Selector



class Category:

    def __init__(self):

        self.flag = 0
        self.url = BASE_URL
        self.main_category = []
        self.document_list = []
        self.mongo_connection = MongoConnection()
        self.category_urls = self.mongo_connection.db[CATEGORY_URLS]
        self.url_404 = self.mongo_connection.db[CATEGORY_404]
        self.url_failed = self.mongo_connection.db[CATEGORY_FAILED]   

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    def request(self):

        url = self.url
        response = requests.get(url,HEADERS)
        if response.status_code == 200:

            logging.info(f'requst successful: {url}')
            if 'commercial' in url:
                self.sub_category_finder(response,url)
            else :    
                self.main_category_finder(response,url)
          
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
                self.request(url)  
            else :
                self.flag = 0 
                try:
                      product_url = {'url':url, 'status':'Failed'}
                      self.url_failed.insert_one(product_url)
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
            logging.info(self.url)
            self.request()
            

        elif url in self.main_category :

            html_data = response.text    
            selector_obj = Selector(html_data)
            main_category_2 = selector_obj.xpath('//a[@title="Properties for rent in Egypt"]/@href').get()
            main_category_2 = "https://www.bayut.eg"+main_category_2
            self.main_category.append(main_category_2)
            
            logging.info(main_category_2)
            self.url = "https://www.bayut.eg/en/egypt/commercial-for-sale/"
            self.request()
           

    def sub_category_finder(self,response,url):

        
        html_data = response.text    
        selector_obj = Selector(html_data)
        next_url = selector_obj.xpath('//a[@title="Commercial Properties for rent in Egypt"]/@href').get()
        print(next_url)
        commercial = selector_obj.xpath('//div[@aria-label="Recommended searches"]/div/a/@href').getall()
        residential = []
        sub_category = selector_obj.xpath('//div[@aria-label="Recommended searches"]/div/div/a/@href').getall()
        logging.info(sub_category)
        key_words = ['apartments','chalets','villas','townhouses','twin-houses','duplexes','penthouses','rooms','residential']
        for item in sub_category:
            for key in key_words:
                if key in item:

                    residential.append(item)
                else :    
                    pass
            if item not in residential:  
                if item not in self.main_category:
                    commercial.append(item)
        logging.info(residential)
        logging.info(commercial)
        for item in self.main_category:
            if 'sale' in item :
                for category in residential:
                    document = {
                        'main cayegory': item,
                        'sub category': item,
                        'end category': "https://www.bayut.eg"+category,
                    }
                    if 'sale' in  category:
                        self.document_list.append(document)  
                    
                for category in commercial:
                    document = {
                        'main cayegory': item,
                        'sub category': url,
                        'end category': "https://www.bayut.eg"+category,   
                    }
                    if 'sale' in  category:
                        self.document_list.append(document)  
                   

            elif 'rent' in item:
                for category in residential:
                    document = {
                        'main cayegory': item,
                        'sub category': item,
                        'end category': "https://www.bayut.eg"+category,
                    }
                    if 'rent' in  category:
                        self.document_list.append(document)  
                    
                for category in commercial:
                    document = {
                        'main cayegory': item,
                        'sub category': url,
                        'end category': "https://www.bayut.eg"+category,   
                    }
                    if 'rent' in  category:
                        self.document_list.append(document)  
                    
       
                           
        if next_url != None:            
            self.url = "https://www.bayut.eg"+(next_url)
            print(self.url)
            self.request() 
        else:
            logging.info('no more catregories')    
        for doc in self.document_list:
                self.category_urls.insert_one(doc)
                logging.info(f'inserted into category_urls: {doc}')
            



if __name__ == '__main__':

    category_obj = Category()
    category_obj.request()        

