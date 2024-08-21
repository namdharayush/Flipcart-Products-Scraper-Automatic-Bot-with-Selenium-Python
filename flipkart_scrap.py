import requests
from lxml import html
import json
import os
import time
from flipkartMongo import Flipkart_Mongo
import re
import pandas as pd

class Flipkart_Scrap:
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://www.flipkart.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-full-version': '"127.0.6533.74"',
            'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.74", "Chromium";v="127.0.6533.74"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
        }
        self.csv_output_file = 'flipcart.csv'
        self.excel_output_file = 'flipcart.xlsx'
        self.json_output_file = 'flipcart.json'

    def scrape(self):
        flipkart_mongo = Flipkart_Mongo()
        flipkart_mongo.create_connections()
        collection = flipkart_mongo.collection
        products = collection.find()
        for product in products:
            print(product['_id'])
            response = requests.get(product['product_link'], headers=self.headers)
            retries = 0
            while 3 > retries and response.status_code != 200:
                print("Retries",retries)
                time.sleep(20)
                response = requests.get(product['product_link'], headers=self.headers)
                if response.status_code == 200:
                    break
                retries += 1
            if retries > 3:
                continue
            sc = html.fromstring(response.text)
            try:
                title = ''.join(sc.xpath("//h1/span/text()"))
            except:
                title = ''
            try:
                images = []
                for all_image in sc.xpath("//ul[@class='ZqtVYK']/li//img/@src"):
                    pattern = r'/(\d+)/(\d+)/'
                    new_dimensions = f"/416/416/"
                    new_image_url = re.sub(pattern,new_dimensions,all_image)
                    images.append(new_image_url)
            except:
                images = ''
            try:
                description = sc.xpath("//div[@class='_4gvKMe']//p/text()")
            except:
                description = ''
            try:
                specification = {}
                for k in sc.xpath("//div[@class='GNDEQ-']"):
                    specification_key = ''.join(k.xpath("./div/text()"))
                    all_keys = k.xpath("./table//tr/td[contains(@class,'+fFi1w')]/text()")
                    all_values = k.xpath("./table//tr/td/ul/li//text()")
                    specification[specification_key] = dict(zip(all_keys,all_values))
                specifications = specification
            except:
                specifications = ''
            try:
                product_descriptions_for_xpath = sc.xpath("//div[text()='Product Description']/parent::div/following-sibling::div")
                product_desc = []
                for product_description in product_descriptions_for_xpath:
                    product_key_4_product_description = ''.join(product_description.xpath(".//div[@class='_9GQWrZ']/text()"))
                    product_desc_4_product_description = ''.join(product_description.xpath(".//div[@class='AoD2-N']/p/text()"))
                    product_img_4_product_description = ''.join(product_description.xpath(".//img/@src"))
                    product_desc.append({'name':product_key_4_product_description,'desc':product_desc_4_product_description,'img':product_img_4_product_description})
            except:
                product_desc = ''
            try:
                rating = ''.join(sc.xpath("(//span[contains(@id,'productRating')]/div[@class='XQDdHH']/text())[1]"))
            except:
                rating = ''
            try:
                price = ''.join(sc.xpath("//div[@class='Nx9bqj CxhGGd']/text()"))
            except:
                price = ''
            try:
                color = ', '.join(sc.xpath("//table//tr/td[contains(text(),'Color')]/following-sibling::td//li/text()"))
            except:
                color = ''
            try:
                storage = ', '.join(sc.xpath("//table//tr/td[contains(text(),'Internal Storage')]/following-sibling::td//li/text()"))
            except:
                storage = ''
            try:
                ram = ', '.join(sc.xpath("//table//tr/td[contains(text(),'RAM')]/following-sibling::td//li/text()"))
            except:
                ram = ''
            try:
                highlights = ', '.join(sc.xpath("//div[@class='vN8oQA']/following-sibling::div//li/text()"))
            except:
                highlights = ''
            data = {
                'title' : title,
                'image' : images,
                'rating' : rating,
                'description' : description,
                'product_desc' : product_desc,
                'specifications' : specifications,
                'price' : price,
                'color' : color,
                'storage' : storage,
                'ram' : ram,
                'highlights' : highlights,
                'status' : 'DONE',
            }
            collection.update_one({'_id':product['_id']},{'$set':data})
            self.create_csv(data)

    def create_csv(self, data):
        df = pd.DataFrame([data])
        if os.path.exists(self.csv_output_file):
            df.to_csv(self.csv_output_file, header=False, index=False, mode='a')
        else:
            df.to_csv(self.csv_output_file, header=True, index=False, mode='a')

    def create_excel(self, data):
        df = pd.DataFrame([data])
        if os.path.exists(self.excel_output_file):
            with pd.ExcelWriter(self.excel_output_file, engine='openpyxl', mode='a',
                                if_sheet_exists='overlay') as writer:
                sheet = writer.sheets.get('Sheet1')
                start_row = sheet.max_row if sheet else 0
                df.to_excel(writer, startrow=start_row, index=False, header=False)
        else:
            df.to_excel(self.excel_output_file, index=False, header=True)

    def create_json(self, data):
        df = pd.DataFrame([data])
        if os.path.exists(self.json_output_file):
            df_existing = pd.read_json(self.json_output_file)
            df_combined = pd.concat([df_existing, df], ignore_index=True)
            df_combined.to_json(self.json_output_file, orient='records', indent=4)
        else:
            df.to_json(self.json_output_file, orient='records', indent=4)

if __name__ == '__main__':
    webscrape = Flipkart_Scrap()
    webscrape.scrape()
