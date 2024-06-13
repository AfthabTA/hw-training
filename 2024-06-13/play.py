import requests
from playwright.sync_api import sync_playwright
from parsel import Selector

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    url = 'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723'
    page.goto(url)
   
    page.click('button[data-aut-id="btnLoadMore"]')
    final_url = page.url
    print(final_url)

    response = requests.get(final_url,headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'})
    if response.status_code == 200:
        print('hai')
        html_data = response.text
        selector_obj = Selector(html_data)
        product = selector_obj.xpath("//li[@data-aut-id='itemBox']")
        n = 0

    else :
        print('bei')

    for data in product:
        
        n +=1
        title = data.xpath(".//span[@data-aut-id='itemTitle']/text()").get()    
        print(n)