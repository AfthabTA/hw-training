import scrapy
# from scrapy.spiders import CrawlSpider,Rule
# from scrapy.linkextractors import LinkExtractor
import json
# from scrapy_splash import SplashRequest
# import requests
# from helium import *
# from bs4 import BeautifulSoup
import pymongo




class olxspider(scrapy.Spider):
    client = pymongo.MongoClient('localhost', 27017)
    db = client["olx_scraper"]
    db_collection = db["olx_data"]

    name = 'olx'

    allowed_domains=['olx.in']

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'}

    start_urls=['https://www.olx.in/api/relevance/v4/search?category=1723&facet_limit=100&lang=en-IN&location=4058877&location_facet_limit=20&page=1&platform=web-desktop&relaxedFilters=true&size=40&user=047405430870509113']

    def parse(self,response):
        data=json.loads(response.body)
        
        
        for property in data['data']:
                
            if property['locations_resolved']['ADMIN_LEVEL_3_name'] == 'Kozhikode':
                place=property['locations_resolved']['SUBLOCALITY_LEVEL_1_name']
            
            else :
                place=property['locations_resolved']['ADMIN_LEVEL_3_name']

            price=property['price']['value']['display']   
            if print is not None:
                        spl_price=price.split()
                        if len(spl_price)>=2:
                                currency=spl_price[0]
                                amount=spl_price[-1]
                                price_dic={'amount':amount,'currency':currency,} 

            images=property['images']
            list_images=[]
            for i in range(len(images)):
                  list_images.append(images[i]['url'])

           

                              
       

            item ={
                'property_name': property['title'],

                'propery_id': property['id'],

                'breadcrumbs': ['Home', 'Properties', 'For Rent: Houses & Apartments', 'For Rent: Houses & Apartments in Kerala', 'For Rent: Houses & Apartments in Kozhikode', 'For Rent: Houses & Apartments in '+place,property['title']],

                'price': price_dic,

                'image_url': list_images,

                'description': property['description'],

                # 'seller_name': ,

                'location': place+','+property['locations_resolved']['ADMIN_LEVEL_3_name']+','+property['locations_resolved']['ADMIN_LEVEL_1_name'],

                'property_type':property['parameters'][0]['value_name'],

                'bathrooms':property['parameters'][2]['value'],

                'bedrooms':property['parameters'][1]['value'],
            }
            
            yield item
            self.db_collection.insert_one(item)    

            # owner=property['user_id']   
            # profile_url='https://www.olx.in/profile/'+owner

            # browser= start_chrome(profile_url, headless=True)
            # soup = BeautifulSoup(browser.page_source, 'html.parser')

            # name=soup.find('div',{'class':'_31kC9'}).Text
            # print(name)

            next_page= data['metadata']['next_page_url']
        if next_page is not None:
                next_page=response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

