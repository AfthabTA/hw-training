import requests
import re
import json
from parsel import Selector 


class Olx:

    def request(self, page, data_list):

        page +=1
        url = f'http://api.olx.in/relevance/v4/search?facet_limit=100&clientId=pwa&clientVersion=10.49.0&platform=web-desktop&size=40&location_facet_limit=20&relaxedFilters=true&location=4058877&page={page}&category=1723&lang=en-IN&user=047405430870509113'
        response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
        print(url)
        print (response)

        if response.status_code == 200:

            json_data=json.loads(response.text)
            print('success')

            if json_data['data'] != []:
                print("working")
                
                for property in json_data['data']:
                    ad_id = property['id']
                    property_url = f"https://www.olx.in/item/{ad_id}"
                    response = requests.get(property_url, headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
                    
                    if response.status_code == 200:
                       
                        html_data = response.text
                        selector_obj = Selector(html_data)


                        item = {

                            'Property_name': selector_obj.xpath("//h1[@data-aut-id='itemTitle']/text()").get(),

                            'Property_id': ad_id,

                            'Breadcrumbs': selector_obj.xpath('//ol[@class="rui-2Pidb"]/li/a/text()').getall(),

                            'Price': selector_obj.xpath('//span[@data-aut-id="itemPrice"]/text()').get(),

                            'Image_url': selector_obj.xpath('//img[@data-aut-id="defaultImg"]/@src').get(),

                            'description': selector_obj.xpath('//div[@data-aut-id="itemDescriptionContent"]/p/text()').getall(),
                            
                            'seller_name': selector_obj.xpath('//div[@class="eHFQs"]/text()').get(),

                            'Location': selector_obj.xpath('//span[@class="_1RkZP"]/text()').get(),

                            'Property_type': selector_obj.xpath('//span[@data-aut-id="value_type"]/text()').get(),

                            'Bathroom': selector_obj.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get(),

                            'Bedroom': selector_obj.xpath('//span[@data-aut-id="value_rooms"]/text()').get(),
                     
                                }
                        print(item)
                        data_list.append(item)

                    else:
                        print("AD not found")


                file_name = "olx_data_new.json"
                with open(file_name, 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)
                    


                self.request(page, data_list)
            else:
                print('End of page')

        else:
            print('Exception occured!!!')






obj = Olx()
obj.request(page = 0, data_list = [])        





