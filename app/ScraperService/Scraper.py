from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime
from app.websites.justjoin import MainPage as Justjoin_MainPage
from app.websites.justjoin import DetailPage as Justjoin_DetailPage
from app.websites.universal import MainPage as Universal_MainPage
from app.websites.universal import DetailPage as Universal_DetailPage


def safe_find_elem(parent, locator):
    text_value = ''
    try:
        text_value = parent.find_element_by_class_name(locator).text
    except Exception as e:
        text_value = ''
    finally:
        return text_value


class Scraper:
    def __init__(self, website:str="", debug:bool=False, service_struct:dict ={}):
        self.service_struct = service_struct
        self.output = {}
        self.debug = debug
        self.website = website
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("-incognito")
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome("./drivers/chromedriver", options=self.options)
        if self.debug: print("Init [", datetime.now(), ']')

    def __del__(self):
        if self.debug: print("Fin [", datetime.now(), ']')
        self.driver.close()

    def get_data(self):
        return self.output

    def set_data(self, data):
        self.output = data

    def run_main_page_scrapping(self, target_number):
        # driver.get(url)  # wczytanie podanej strony
        if self.website == "https://justjoin.it/":
            main_page = Justjoin_MainPage.MainPage(self.driver)
            if self.debug: print("Main Page [START : ", datetime.now(), ']')
            self.output = main_page.get_n_offers_from_list(target_number)
            if self.debug: print("Main Page [END : ", datetime.now(), ']')
            if self.debug: print("Number of elements: ", self.output.__len__())
            # print(list(self.output.keys())[0])
        else:
            custom_page = Universal_MainPage.MainPage(self.driver, self.service_struct["main_page"])
            self.output = custom_page.get_n_offers_from_list(target_number)
        return self.output

    def run_detail_page_scrapping(self, target_id):

        if self.debug: print("Detail Page [START : ", datetime.now(), ']')

        if self.website == "https://justjoin.it/":
            detail_page = Justjoin_DetailPage.DetailPage(self.driver, target_id, debug=self.debug)
            detail_data = detail_page.get_data()
        else:
            custom_page = Universal_DetailPage.DetailPage(self.driver, target_id, self.service_struct["detail_page"], debug=self.debug)
            detail_data = custom_page.get_data()

        self.output[target_id] = {}
        self.output[target_id]['title'] = detail_data[target_id]['title']
        self.output[target_id]['salary'] = detail_data[target_id]['salary']
        self.output[target_id]['salary_from'] = detail_data[target_id]['salary_from']
        self.output[target_id]['salary_to'] = detail_data[target_id]['salary_to']
        self.output[target_id]['currency'] = detail_data[target_id]['currency']
        self.output[target_id]['street'] = detail_data[target_id]['street']
        self.output[target_id]['city'] = detail_data[target_id]['city']
        self.output[target_id]['employer'] = detail_data[target_id]['employer']
        self.output[target_id]['experience'] = detail_data[target_id]['experience']
        self.output[target_id]['employment'] = detail_data[target_id]['employment']
        self.output[target_id]['description'] = detail_data[target_id]['description']
        if self.debug: print("Detail Page [END : ", datetime.now(), ']')

    def save_data(self):
        if self.debug: print("Save [START : ", datetime.now(), ']')
        json_data = json.dumps(self.output)
        f = open("../../dict.json", "w")
        f.write(json_data)
        f.close()
        if self.debug: print("Save [END : ", datetime.now(), ']')
