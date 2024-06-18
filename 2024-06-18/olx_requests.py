import requests
import re
import json
from parsel import Selector 
# from urllib.parse import urljoin

class Olx:
    
    
    def request(self, next_page,data_list):

       
        
        flag = 0

       
        if next_page == 1:
            
            url = ('http://api.olx.in/relevance/v4/search?facet_limit=100&clientId=pwa&clientVersion=10.49.0&platform=web-desktop&size=40&location_facet_limit=20&relaxedFilters=true&location=4058877&page=2&category=1723&lang=en-IN&user=047405430870509113')
            response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
        elif next_page != None:
              print(next_page)
              response = requests.get(next_page, headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
        elif next_page == None:
            print('***END')
            
        
            
        if response.status_code == 200:

            next_page = None

            json_data=json.loads(response.text)
            print('success')

            if json_data['data'] != []:
                for property in json_data['data']:
                        if flag == 1:
                            print("****** END OF PAGE ******")
                            
                        else :
                    
                            if 'SUBLOCALITY_LEVEL_1_name' == list(property['locations_resolved'].keys())[-1]:
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

                            # print(item)

                            next_page= json_data['metadata']['next_page_url']
                        data_list.append(item)

                
                file_name = "olx_data.json"
                with open(file_name, 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)
                    self.request(next_page,data_list)

            else:
                 print("***END***")
                 next_page = None
                 self.request(next_page,data_list)

        else :
            print('exception occured!!!')  
            file_name = "olx_data.json"
            with open(file_name, 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)  
            

obj = Olx()
obj.request(next_page = 1,data_list = [])





