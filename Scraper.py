from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime


def safe_find_elem(parent, locator):
    text_value = ''
    try:
        text_value = parent.find_element_by_class_name(locator).text
    except Exception:
        text_value = ''
    finally:
        return text_value


class Scraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("-incognito")
        self.options.add_argument('headless')

    def run(self, url, target_number):
        print("Inicjalizacja [", datetime.now(), ']')
        driver = webdriver.Chrome("./drivers/chromedriver", options=self.options)
        driver.get(url)  # wczytanie podanej strony

        root = driver.find_element_by_class_name('css-110u7ph')
        location = root.location
        size = root.size
        scrollbar_x = location['x'] + size['width'] - size['width'] / 100
        scrollbar_y = location['y'] + 90

        output = {}  # dane wyjściowe
        move_number = 0
        end_flag = 0
        print("Wczytanie danych [START : ", datetime.now(), ']')
        while end_flag == 0:
            attempts = 0
            while attempts < 3:
                try:
                    lista = driver.find_element_by_xpath(
                        '//*[@id="root"]/div[3]/div[1]/div/div[2]')  # lista elementów znaleziona dzięki xpath
                    elem = lista.find_elements_by_tag_name("a")  # ogłoszenia znalezione po tagu 'a'

                    # przeszukujemy ogłoszenie w poszukiwaniu konkretnych elementów
                    for x in elem:
                        if output.__len__() >= target_number:
                            end_flag = 1
                            break
                        else:
                            output[x.get_attribute("href").__str__().replace('https://justjoin.it/offers/', '')] = {
                                'title': safe_find_elem(x, 'css-wjfk7i'),
                                'info': safe_find_elem(x, 'css-jbk0sa'),
                                'salary': safe_find_elem(x, 'css-1dotj4s'),
                                'status': safe_find_elem(x, 'css-hw5uoy')
                            }
                    if end_flag == 1:
                        break
                    action = ActionChains(driver)
                    if move_number == 0:
                        action.move_by_offset(scrollbar_x, scrollbar_y).click().perform()
                        move_number = 1
                    elif move_number >= 1:
                        action.send_keys(Keys.PAGE_DOWN).perform()
                        move_number += 1
                except Exception:
                    attempts += 1
        print("Wczytanie danych [END : ", datetime.now(), ']')
        print("Liczba wczytanych elementów: ", output.__len__())
        # print("Zapis do pliku [START : ", datetime.now(), ']')
        json_data = json.dumps(output)
        f = open("dict.json", "w")
        f.write(json_data)
        f.close()
        print("Zapis do pliku [END : ", datetime.now(), ']')
        time.sleep(3)
        driver.close()
