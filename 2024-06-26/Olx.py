import requests
import re
import json
from parsel import Selector 


class Olx:

    def filter(self, filter_selector,data_list):
         page = 0
         filter_list = ["type=houses","type=rent-apartments","type=floors"]
         if filter_selector<len(filter_list):
            self.url_filter = filter_list[filter_selector]
            print(self.url_filter)
            obj.request(data_list, filter_selector, page )
         else:
              print("No more filters!!!")
         

    def request(self, data_list, filter_selector, page):
        page +=1



        url = f'http://api.olx.in/relevance/v4/search?facet_limit=100&clientId=pwa&clientVersion=10.50.0&platform=web-desktop&size=40&location_facet_limit=20&relaxedFilters=true&location=4058877&page={page}&category=1723&lang=en-IN&user=047405430870509113&'+self.url_filter
        response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
        print(url)
        print (response)

        if response.status_code == 200:

            self.json_data=json.loads(response.text)
            print('success')

            if self.json_data['data'] != []:
                print("working")
                obj.parse(page, data_list, filter_selector)

            else:
                print('End of page') 
                filter_selector += 1
                obj.filter(filter_selector, data_list ) 

        else:
            print('Exception occured!!!')          
                
    def parse(self,page, data_list, filter_selector):


                for property in self.json_data['data']:
                    ad_id = property['id']
                    property_url = f"https://www.olx.in/item/{ad_id}"
                    response = requests.get(property_url, headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
                    
                    if response.status_code == 200:
                       
                        html_data = response.text
                        selector_obj = Selector(html_data)

                        price = selector_obj.xpath('//span[@data-aut-id="itemPrice"]/text()').get()
                        if price is not None:
                            spl_price=price.split()
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

                            'property_name': selector_obj.xpath("//h1[@data-aut-id='itemTitle']/text()").get(),

                            'property_id': ad_id,

                            'breadcrumbs': selector_obj.xpath('//ol[@class="rui-2Pidb"]/li/a/text()').getall(),

                            'price': price_dic,

                            'image_url': selector_obj.xpath('//img[@data-aut-id="defaultImg"]/@src').get(),

                            'description': selector_obj.xpath('//div[@data-aut-id="itemDescriptionContent"]/p/text()').getall(),
                            
                            'seller_name': selector_obj.xpath('//div[@class="eHFQs"]/text()').get(),

                            'location': selector_obj.xpath('//span[@class="_1RkZP"]/text()').get(),

                            'property_type': selector_obj.xpath('//span[@data-aut-id="value_type"]/text()').get(),

                            'bathrooms': int(num_bathroom),

                            'bedrooms': int(num_bedroom)
                     
                                }
                        print(item)
                        data_list.append(item)

                    else:
                        print("AD not found")


                file_name = "olx_data_new1.json"
                with open(file_name, 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)
                    


                self.request(data_list, filter_selector, page)
            

        






obj = Olx()
obj.filter(filter_selector = 0, data_list = [])      

# https://api.olx.in/relevance/v4/search?facet_limit=1000&clientId=pwa&type=houses&clientVersion=10.50.0&platform=web-desktop&size=40&location_facet_limit=20&relaxedFilters=true&location=4058877&page=1&category=1723&lang=en-IN&user=006801545593302671
# https://www.olx.in/api/relevance/v4/search?category=1723&facet_limit=1000&lang=en-IN&location=4058877&location_facet_limit=20&page=1&platform=web-desktop&relaxedFilters=true&rooms=1%2B&size=40&user=006801545593302671

# type=rent-apartments
# type=houses
# type=floors
# rooms=1%2B