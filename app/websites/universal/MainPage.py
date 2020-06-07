from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime


class MainPageLocators:
    @staticmethod
    def get_by(by_type):
        if by_type == "tag_name":
            return By.TAG_NAME
        elif by_type == "class_name":
            return By.CLASS_NAME
        elif by_type == "xpath":
            return By.XPATH

    def __init__(self, locators_dict: dict):
        self.offer_list = (self.get_by(locators_dict["offer_list"]["by"]), locators_dict["offer_list"]["locator"])
        self.offer = (self.get_by(locators_dict["offer"]["by"]), locators_dict["offer"]["locator"])
        self.offer_title = (self.get_by(locators_dict["offer_title"]["by"]), locators_dict["offer_title"]["locator"])
        self.offer_url = (self.get_by(locators_dict["offer_url"]["by"]), locators_dict["offer_url"]["locator"])

    # LIST_SCROLLBAR = (By.CLASS_NAME, 'css-110u7ph')
    # LIST = (By.XPATH, '//*[@id="root"]/div[3]/div[1]/div/div[2]')
    # OFFER = (By.TAG_NAME, 'a')
    # OFFER_TITLE = (By.CLASS_NAME, 'css-wjfk7i')
    # OFFER_INFO = (By.CLASS_NAME, 'css-jbk0sa')
    # OFFER_SALARY = (By.CLASS_NAME, 'css-1dotj4s')
    # OFFER_STATUS = (By.CLASS_NAME, 'css-hw5uoy')


class MainPage:
    def __init__(self, driver, uni_dict):
        self.main_page_dict = uni_dict
        self.locators = MainPageLocators(self.main_page_dict)
        self.list_type = self.main_page_dict["list_type"]
        self.url = self.main_page_dict["url"]

        self.offer_list = {}
        self.driver = driver
        self.driver.get(self.url)
        self.scrollbar_x = 0
        self.scrollbar_y = 0
        self.find_list_scrollbar_pos()

    def find_list_scrollbar_pos(self):
        try:
            list_root = self.driver.find_element(*MainPageLocators.LIST_SCROLLBAR)
            location = list_root.location
            size = list_root.size
            self.scrollbar_x = location['x'] + size['width'] - size['width'] / 100
            self.scrollbar_y = location['y'] + 90
        except:
            pass

    def get_n_offers_from_list(self, n):
        def find(parent, locator):
            text_value = ''
            try:
                text_value = parent.find_element(*locator).text
            except Exception as e:
                text_value = ''
            finally:
                return text_value

        output = {}  # dane wyjściowe
        move_number = 0
        end_flag = 0
        page = 1
        if self.list_type == "inf":
            while end_flag == 0:
                attempts = 0
                while attempts < 3:
                    try:
                        offer_list = self.driver.find_element(self.locators.offer_list)
                        elem = offer_list.find_elements(self.locators.offer)
                        # przeszukujemy ogłoszenie w poszukiwaniu konkretnych elementów
                        for x in elem:
                            if output.__len__() >= n:
                                end_flag = 1
                                break
                            else:
                                output[x.get_attribute("href").__str__()] = {
                                    'title': find(x, self.locators.offer_title),
                                }
                        if end_flag == 1:
                            break
                        action = ActionChains(self.driver)
                        if move_number == 0:
                            action.move_by_offset(self.scrollbar_x, self.scrollbar_y).click().perform()
                            move_number = 1
                        elif move_number >= 1:
                            action.send_keys(Keys.PAGE_DOWN).perform()
                            move_number += 1
                    except Exception:
                        attempts += 1
            self.offer_list = output

        elif self.list_type == "pagination":
            while end_flag == 0:
                attempts = 0
                while attempts < 3:
                    offer_list = self.driver.find_element(*self.locators.offer_list)
                    elem = offer_list.find_elements(*self.locators.offer)
                    # przeszukujemy ogłoszenie w poszukiwaniu konkretnych elementów
                    for x in elem:
                        if output.__len__() >= n:
                            end_flag = 1
                            break
                        else:
                            if self.main_page_dict['url'] in x.get_attribute("href").__str__():
                                # print(x.get_attribute("href").__str__())
                                output[x.get_attribute("href").__str__()] = {
                                    'title': find(x, self.locators.offer_title),
                                }
                    if len(elem) < n:
                        page += 1
                        self.driver.get(self.url+"?page="+page)
                    if end_flag == 1:
                        break
            self.offer_list = output
        return output
