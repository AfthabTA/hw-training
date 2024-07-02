import requests
import re
import json
from parsel import Selector 
import multiprocessing


class Olx:

    def __init__(self):
        self.parsed_data_list = multiprocessing.Manager().list()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'     
            }

    def filter(self, filter_selector,data_list, url_list):
         page = 0
         filter_list = ["type=houses","type=rent-apartments","type=floors","rooms=1%2B","rooms=2%2B","rooms=3%2B","rooms=4%2B",
                        "furnished=yes","furnished=no","furnished=semi","listed_by=owner","listed_by=broker","bachelors=yes",
                        "bachelors=no","price_max=50000","price_max=100000"]
         if filter_selector<len(filter_list):
            self.url_filter = filter_list[filter_selector]
            print(self.url_filter)
            obj.request(data_list, filter_selector, page ,url_list)
         else:
              print("No more filters!!!")
              file_name = "url_list.json"
              with open(file_name, 'w') as json_file:
                     json.dump(url_list, json_file, indent = 4)


              num_processes = multiprocessing.cpu_count()

              with multiprocessing.Pool(processes=num_processes) as pool:
                    pool.starmap(self.parse, [(data_list, url) for url in url_list]) 

              big_list = list(self.parsed_data_list) 
              file_name = "data_final.json"
              with open(file_name, 'w') as json_file:
                     json.dump(big_list, json_file, indent = 4)    

    def request(self, data_list, filter_selector, page, url_list):

        page +=1

        url = f'http://api.olx.in/relevance/v4/search?facet_limit=100&clientId=pwa&clientVersion=10.50.0&platform=web-desktop&size=40&location_facet_limit=20&relaxedFilters=true&location=4058877&page={page}&category=1723&lang=en-IN&user=047405430870509113&'+self.url_filter
        response = requests.get(url, headers = self.headers)
        print(url)
        print (response)

        if response.status_code == 200:

            self.json_data=json.loads(response.text)
            print('success')

            if self.json_data['data'] != []:
                print("working")
                for property in self.json_data['data']:
                    ad_id = property['id']
                    property_url = f"https://www.olx.in/item/{ad_id}"
                    
                    if property_url in url_list:
                         print("\n!!!Data already exists!!!")
                         print("\n",ad_id)
                         continue
                    url_list.append(property_url) 
                    file_name = "url_list.json"
                    with open(file_name, 'w') as json_file:
                        json.dump(url_list, json_file, indent = 4)
                  
                self.request(data_list, filter_selector, page, url_list )

            else:
                print('End of page') 
                filter_selector += 1
                obj.filter(filter_selector, data_list, url_list ) 

        else:
            print('Exception occured!!!')          
                
    def parse(self, data_list, url):

                    response = requests.get(url, headers = self.headers)
                    
                    if response.status_code == 200:
                       
                        html_data = response.text
                        selector_obj = Selector(html_data)

                        Ad_id = url.rsplit('/',1)[-1]

                        Title = selector_obj.xpath("//h1[@data-aut-id='itemTitle']/text()").get()

                        Breadcrumbs = selector_obj.xpath('//div[@data-aut-id="breadcrumb"]/div/ol/li/a/text()').getall()

                        Price = selector_obj.xpath('//span[@data-aut-id="itemPrice"]/text()').get()

                        Image = selector_obj.xpath('//img[@data-aut-id="defaultImg"]/@src').get()

                        Description = selector_obj.xpath('//div[@data-aut-id="itemDescriptionContent"]/p/text()').getall()

                        Seller = selector_obj.xpath('//div[@data-aut-id="profileCard"]/div/a/div/text()').get()

                        Location = selector_obj.xpath('//div[@data-aut-id="itemLocation"]/div/span/text()').get()

                        Property_type = selector_obj.xpath('//span[@data-aut-id="value_type"]/text()').get()


                        if Price is not None:
                            spl_price=Price.split()
                            if len(spl_price)>=2:
                                currency=spl_price[0]
                                amount=spl_price[-1]
                                price_dic={'amount':amount,'currency':currency,}

                        else :
                             price_dic={'amount':"",'currency':"₹",}

                        bathroom =  selector_obj.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get()
                        if bathroom != None:
                            num_bathroom = bathroom.rstrip('+')
                        else :
                             num_bathroom = 0    

                        bedroom = selector_obj.xpath('//span[@data-aut-id="value_rooms"]/text()').get()
                        if bedroom != None:
                            num_bedroom = bedroom.rstrip('+')
                        else :
                             num_bedroom = 0 

                        item = {

                            'property_name': Title,

                            'property_id': Ad_id,

                            'breadcrumbs': Breadcrumbs,

                            'price': price_dic,

                            'image_url': Image,

                            'description': Description,
                            
                            'seller_name': Seller,

                            'location': Location,

                            'property_type': Property_type,

                            'bathrooms': int(num_bathroom),

                            'bedrooms': int(num_bedroom)
                     
                                }
                        print(item)
                        
                        self.parsed_data_list.append(item)
                        
                        

                    else:
                        print("AD not found")


if __name__ == '__main__':

    obj = Olx()
    obj.filter(filter_selector = 0, data_list = [], url_list =[])      





# https://api.olx.in/relevance/v4/search?facet_limit=1000&clientId=pwa&type=houses&clientVersion=10.50.0&platform=web-desktop&size=40&location_facet_limit=20&relaxedFilters=true&location=4058877&page=1&category=1723&lang=en-IN&user=006801545593302671

# furnished=semi
# type=rent-apartments
# type=houses
# type=floors
# rooms=1%2B
# rooms=2%2B
# rooms=3%2B
# rooms=4%2B
# furnished=yes
# furnished=no
# furnished=semi
# listed_by=owner
# listed_by=broker
# bachelors=yes
# bachelors=no
# price_max=100000

# with concurrent.futures.ThreadPoolExecutor() as executor:
#                    executor.map(self.parse, url_list)