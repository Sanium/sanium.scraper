from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


class DetailPageLocators:
    OFFER_TITLE = (By.CLASS_NAME, 'css-1v15eia')
    OFFER_SALARY = (By.CLASS_NAME, 'css-8cywu8')
    OFFER_LOCATION = (By.CLASS_NAME, 'css-1d6wmgf')
    COMPANY_LOGO = (By.CLASS_NAME, 'css-17jro83')
    COMPANY_NAME = (By.CLASS_NAME, 'css-l4opor')
    #TODO: inny typ lokalizacji dla exp i emp
    OFFER_EXPERIENCE = (By.CLASS_NAME, 'css-1ji7bvd')
    OFFER_EMPLOYMENT = (By.CLASS_NAME, 'css-1ji7bvd')
    OFFER_DESCRIPTION = (By.CLASS_NAME, 'css-u2qsbz')


class DetailPage:
    def __init__(self, driver, key):
        self.driver = driver
        self.key = key
        self.url = "https://justjoin.it/offers/" + self.key
        self.driver.get(self.url)

    def get_data(self):
        def find(parent, locator):
            text_value = ''
            try:
                text_value = parent.find_element(*locator).text
            except Exception as e:
                print(e)
                text_value = ''
            finally:
                return text_value

        def find_list(parent, locator):
            try:
                temp_list = parent.find_elements(*locator)
                output_list = [x.text for x in temp_list]
                return output_list
            except Exception as e:
                print(e)

        output = {}  # dane wyjściowe
        print("Wczytanie oferty [START : ", datetime.now(), ']')
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(DetailPageLocators.OFFER_TITLE))

        title = self.driver.find_element(*DetailPageLocators.OFFER_TITLE).text
        basic = find_list(self.driver, DetailPageLocators.OFFER_EXPERIENCE),
        company_size = basic[0][0]
        employment = basic[0][1]
        experience = basic[0][2]
        output[self.key] = {
            'title': title,
            'salary': find(self.driver, DetailPageLocators.OFFER_SALARY),
            'location': find(self.driver, DetailPageLocators.OFFER_LOCATION),
            'employer': find(self.driver, DetailPageLocators.COMPANY_NAME),
            'experience': experience,
            'employment': employment,
            'description': find(self.driver, DetailPageLocators.OFFER_DESCRIPTION)

        }
        print("Wczytanie oferty [END : ", datetime.now(), ']')
        return output
