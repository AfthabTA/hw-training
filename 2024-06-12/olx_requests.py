import requests
import re
import json
from parsel import Selector 

class Olx:

    def request():

        data_list = []
        url = ('https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723')
        response = requests.get(url,headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})

        if response.status_code == 200:
            html_data = response.text
            selector_obj = Selector(html_data)
            product = selector_obj.xpath("//li[@data-aut-id='itemBox']")
        else :
            print('exception occured!!!')    

        for data in product:  

            title = data.xpath(".//span[@data-aut-id='itemTitle']/text()").get()
            product_link = data.css("a::attr(href)").get()

            if product_link != None:
                product_url = 'https://www.olx.in'+product_link
                response = requests.get(product_url,headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
                html_data = response.text
                selector_new = Selector(html_data)

                property_id = selector_new.xpath('//div[@class="_1-oS0"]/strong').re(r'\d+')
                


                breadcrumbs = selector_new.xpath('//ol[@class="rui-2Pidb"]/li/a/text()').getall()
            
                price = selector_new.xpath('//span[@data-aut-id="itemPrice"]/text()').get()

                img = selector_new.xpath('//img[@data-aut-id="defaultImg"]/@src').get()

                description = selector_new.xpath('//div[@data-aut-id="itemDescriptionContent"]/p/text()').getall()

                seller_name = selector_new.css('div.eHFQs::text').get()

                location = selector_new.css('span._1RkZP::text').get()

                property_type = selector_new.xpath('//span[@data-aut-id="value_type"]/text()').get()
                
                bathrooms = selector_new.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get()

                bedrooms = selector_new.xpath('//span[@data-aut-id="value_rooms"]/text()').get()

                item = {
                    'Property_name': title,
                    'Property_id': property_id,
                    'Breadcrumbs': breadcrumbs,
                    'Price': price,
                    'Image_url':img,
                    'description': description,
                    'seller_name': seller_name,
                    'Location': location,
                    'Property_type': property_type,
                    'Bathroom': bathrooms,
                    'Bedroom': bedrooms,
                     
                }

                print(item)
                data_list.append(item)

                file_name = "olx_data.json"
                with open(file_name, 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)

        
Olx.request()         

   

