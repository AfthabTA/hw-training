import requests
from parsel import Selector 

class Olx:

    def request():

        url = ('https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723')
        response = requests.get(url,headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
        if response.status_code == 200:
            # print (response.text)
            html_data = response.text
            selector_obj = Selector(html_data)
            product = selector_obj.xpath("//li[@data-aut-id='itemBox']")
            # print(product)
        else :
            print('exception occured!!!')    

        for data in product:   
            title = data.xpath("//span[@data-aut-id='itemTitle']/text()").get()  
            product_link = data.xpath("//a[@class='_2cbZ2']/@href").get()
        print(title)

        print(product_link)
        
Olx.request()         

   


