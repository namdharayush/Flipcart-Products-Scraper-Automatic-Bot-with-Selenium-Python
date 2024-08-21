import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flipcartMongo import Flipcart_Mongo
class Flipcart:
    def __init__(self):
        self.main_url = 'https://www.flipkart.com/'
        self.driver = self.start_driver(self.main_url)
    def start_driver(self, url):
        chrome_options = Options()
        service = Service()
        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.maximize_window()
        driver.get(url)
        return driver
    def scrape_with_selenium(self):
        Flipcart_mongoDb = Flipcart_Mongo()
        # keywords = ['redmi mobiles','samsung mobiles','iphone','vivo mobiles','oppo mobiles']
        keywords = ['samsung mobiles','iphone','vivo mobiles','oppo mobiles']
        for keyword in keywords:
            try:
                input_search = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//form[contains(@class,'header-form-search')]//input[@name='q']")))
                time.sleep(1)
                input_search.click()
                input_search.clear()
                input_search.send_keys(keyword)
            except Exception as e:
                print(e)
            time.sleep(1)
            try:
                search_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//form[contains(@class,'header-form-search')]//button")))
                search_button.click()
            except Exception as e:
                print(e)
            time.sleep(1)
            page = 1
            while True:
                print(page)
                all_products = self.driver.find_elements(By.XPATH, "//div[@class = '_75nlfW']//a")
                if not all_products:
                    break
                for all_product in all_products:
                    try:
                        product_link = all_product.get_attribute("href")
                    except:
                        product_link = ''
                    try:
                        Flipcart_mongoDb.insert_data({'product_link': product_link})
                    except:
                        print("Duplicate")
                try:
                    next_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='_9QVEpD']/span[contains(text(),'Next')]")))
                    next_button.click()
                    time.sleep(2)
                except:
                    break
                page +=1
            self.driver.refresh()
            try:
                self.driver.find_element(By.XPATH,"//span[@class='_30XB9F']").click()
            except:
                pass

if __name__ == '__main__':
    webscrapper = Flipcart()
    webscrapper.scrape_with_selenium()

