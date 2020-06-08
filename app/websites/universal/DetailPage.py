from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import re


class DetailPageLocators:
    @staticmethod
    def get_by(by_type):
        if by_type == "tag_name":
            return By.TAG_NAME
        elif by_type == "class_name":
            return By.CLASS_NAME
        elif by_type == "xpath":
            return By.XPATH

    def __init__(self, locators_dict: dict):
        self.offer_title = (self.get_by(locators_dict["offer_title"]["by"]), locators_dict["offer_title"]["locator"])
        self.offer_technology = (
        self.get_by(locators_dict["offer_technology"]["by"]), locators_dict["offer_technology"]["locator"])
        self.offer_salary = (self.get_by(locators_dict["offer_salary"]["by"]), locators_dict["offer_salary"]["locator"])
        self.offer_salary_currency = (
        self.get_by(locators_dict["offer_salary_currency"]["by"]), locators_dict["offer_salary_currency"]["locator"])
        self.offer_location = (
        self.get_by(locators_dict["offer_location"]["by"]), locators_dict["offer_location"]["locator"])
        self.offer_experience = (
        self.get_by(locators_dict["offer_experience"]["by"]), locators_dict["offer_experience"]["locator"])
        self.offer_employment = (
        self.get_by(locators_dict["offer_employment"]["by"]), locators_dict["offer_employment"]["locator"])
        self.offer_description = (
        self.get_by(locators_dict["offer_description"]["by"]), locators_dict["offer_description"]["locator"])
        self.company_logo = (self.get_by(locators_dict["company_logo"]["by"]), locators_dict["company_logo"]["locator"])
        self.company_name = (self.get_by(locators_dict["company_name"]["by"]), locators_dict["company_name"]["locator"])

    # OFFER_TITLE = (By.CLASS_NAME, 'css-1v15eia')
    # OFFER_SALARY = (By.CLASS_NAME, 'css-8cywu8')
    # OFFER_LOCATION = (By.CLASS_NAME, 'css-1d6wmgf')
    # COMPANY_LOGO = (By.CLASS_NAME, 'css-17jro83')
    # COMPANY_NAME = (By.CLASS_NAME, 'css-l4opor')
    # # TODO: inny typ lokalizacji dla exp i emp
    # OFFER_EXPERIENCE = (By.CLASS_NAME, 'css-1ji7bvd')
    # OFFER_EMPLOYMENT = (By.CLASS_NAME, 'css-1ji7bvd')
    # OFFER_DESCRIPTION = (By.CLASS_NAME, 'css-u2qsbz')


class DetailPage:
    def __init__(self, driver, url, uni_dict, debug=False):
        self.driver = driver
        self.detail_page_dict = uni_dict
        self.locators = DetailPageLocators(self.detail_page_dict)

        self.url = url
        self.driver.get(self.url)
        self.debug = debug

    @staticmethod
    def format_salary(salary):
        if type(salary) is tuple:
            salary = salary[0]
        from_to = re.findall(r'([\d ]+)', salary)
        currency = re.findall(r'([A-Z]+)', salary)
        if len(from_to) >= 2:
            salary_from = from_to[0].replace(' ', '')
            salary_to = from_to[1].replace(' ', '')
            if len(currency) >= 1 and len(currency[0]) == 3:
                currency = currency[0]
                salary = '%s %s %s' % (salary_from, salary_to, currency)
                return {'salary': salary, 'salary_from': salary_from, 'salary_to': salary_to, 'currency': currency}
            else:
                salary = '%s %s' % (salary_from, salary_to)
                return {'salary': salary, 'salary_from': salary_from, 'salary_to': salary_to, 'currency': None}
        else:
            return {'salary': salary.strip(), 'salary_from': None, 'salary_to': None, 'currency': None}

    @staticmethod
    def format_location(location):
        if type(location) is tuple:
            location = location[0]

        location = location.split(',')
        if len(location) >= 2:
            city = location[1]
            street = location[0]
            return {'city': city, 'street': street}
        elif len(location[0]) > 0:
            return {'city': location[0], 'street': None}
        else:
            return {'city': None, 'street': None}

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
        if self.debug: print("Wczytanie oferty [START : ", datetime.now(), ']')
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.locators.offer_title))
        except TimeoutException:
            return None
        title = self.driver.find_element(*self.locators.offer_title).text
        basic = find_list(self.driver, self.locators.offer_experience),

        salary = find(self.driver, self.locators.offer_salary)
        print(salary)
        salary = self.format_salary(salary)
        employment = self.driver.find_element(*self.locators.offer_employment).text
        experience = self.driver.find_element(*self.locators.offer_experience).text
        location = find(self.driver, self.locators.offer_location)
        location = self.format_location(location)

        output[self.url] = {
            'title': title,
            'salary': salary['salary'],
            'salary_from': salary['salary_from'] if salary['salary_from'] is not None else "",
            'salary_to': salary['salary_to'] if salary['salary_to'] is not None else "",
            'currency': salary["currency"] if salary["currency"] is not None else "",
            'street': location['street'] if location['street'] is not None else "",
            'city': location['city'] if location['city'] is not None else "",
            'employer': find(self.driver, self.locators.company_name),
            'experience': experience if experience is not None else "",
            'employment': employment if employment is not None else "",
            'description': find(self.driver, self.locators.offer_description)
        }
        if self.debug: print("Wczytanie oferty [END : ", datetime.now(), ']')
        return output
