from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime
from app.websites.justjoin import MainPage as Justjoin_MainPage
from app.websites.justjoin import DetailPage as Justjoin_DetailPage


def safe_find_elem(parent, locator):
    text_value = ''
    try:
        text_value = parent.find_element_by_class_name(locator).text
    except Exception as e:
        text_value = ''
    finally:
        return text_value


class Scraper:
    def __init__(self):
        print("Init [", datetime.now(), ']')
        self.output = {}
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("-incognito")
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome("./drivers/chromedriver", options=self.options)

    def __del__(self):
        print("Fin [", datetime.now(), ']')
        self.driver.close()

    def run_main_page_scrapping(self, url, target_number):
        # driver.get(url)  # wczytanie podanej strony
        if url == "https://justjoin.it/":
            main_page = Justjoin_MainPage.MainPage(self.driver)
            print("Main Page [START : ", datetime.now(), ']')
            self.output = main_page.get_n_offers_from_list(target_number)
            print("Main Page [END : ", datetime.now(), ']')
            print("Number of elements: ", self.output.__len__())
            # print(list(self.output.keys())[0])
        return self.output

    def run_detail_page_scrapping(self):
        print("Detail Page [START : ", datetime.now(), ']')
        for i in range(self.output.__len__()):
            detail_page = Justjoin_DetailPage.DetailPage(self.driver, list(self.output.keys())[i])
            detail_data = detail_page.get_data()
            self.output[list(self.output.keys())[i]]['location'] = detail_data[list(self.output.keys())[i]]['location']
            self.output[list(self.output.keys())[i]]['employer'] = detail_data[list(self.output.keys())[i]]['employer']
            self.output[list(self.output.keys())[i]]['experience'] = detail_data[list(self.output.keys())[i]]
            ['experience']
            self.output[list(self.output.keys())[i]]['employment'] = detail_data[list(self.output.keys())[i]]
            ['employment']
            self.output[list(self.output.keys())[i]]['description'] = detail_data[list(self.output.keys())[i]]
            ['description']
        print("Detail Page [END : ", datetime.now(), ']')

    def save_data(self):
        print("Save [START : ", datetime.now(), ']')
        json_data = json.dumps(self.output)
        f = open("../../dict.json", "w")
        f.write(json_data)
        f.close()
        print("Save [END : ", datetime.now(), ']')