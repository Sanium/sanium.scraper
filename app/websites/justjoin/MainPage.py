from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime


class MainPageLocators:
    LIST_SCROLLBAR = (By.CLASS_NAME, 'css-110u7ph')
    LIST = (By.XPATH, '//*[@id="root"]/div[3]/div[1]/div/div[2]')
    OFFER = (By.TAG_NAME, 'a')
    OFFER_TITLE = (By.CLASS_NAME, 'css-wjfk7i')
    OFFER_INFO = (By.CLASS_NAME, 'css-jbk0sa')
    OFFER_SALARY = (By.CLASS_NAME, 'css-1dotj4s')
    OFFER_STATUS = (By.CLASS_NAME, 'css-hw5uoy')


class MainPage:
    def __init__(self, driver):
        self.offer_list = {}
        self.driver = driver
        self.url = "https://justjoin.it/"
        self.driver.get(self.url)
        self.scrollbar_x = 0
        self.scrollbar_y = 0
        self.find_list_scrollbar_pos()

    def find_list_scrollbar_pos(self):
        list_root = self.driver.find_element(*MainPageLocators.LIST_SCROLLBAR)
        location = list_root.location
        size = list_root.size
        self.scrollbar_x = location['x'] + size['width'] - size['width'] / 100
        self.scrollbar_y = location['y'] + 90

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
        while end_flag == 0:
            attempts = 0
            while attempts < 3:
                try:
                    offer_list = self.driver.find_element(*MainPageLocators.LIST) # lista elementów znaleziona dzięki xpath
                    elem = offer_list.find_elements(*MainPageLocators.OFFER)  # ogłoszenia znalezione po tagu 'a'
                    # przeszukujemy ogłoszenie w poszukiwaniu konkretnych elementów
                    for x in elem:
                        if output.__len__() >= n:
                            end_flag = 1
                            break
                        else:
                            output[x.get_attribute("href").__str__().replace('https://justjoin.it/offers/', '')] = {
                                'title': find(x, MainPageLocators.OFFER_TITLE),
                                # 'info': find(x, MainPageLocators.OFFER_INFO),
                                # 'salary': find(x, MainPageLocators.OFFER_SALARY),
                                # 'status': find(x, MainPageLocators.OFFER_STATUS)
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
        return output
