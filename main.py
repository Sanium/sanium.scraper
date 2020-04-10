import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

option = webdriver.ChromeOptions()
option.add_argument("-incognito")

driver = webdriver.Chrome("C:\\Users\\ReQezeR\\Desktop\\chromedriver", options=option)
driver.get("https://justjoin.it/")  # wczytanie podanej strony

lista = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[1]/div/div[2]')    # lista elementów znaleziona dzięki xpath

elem = lista.find_elements_by_tag_name("a")     # ogłoszenia znalezione po tagu 'a'
print("Wczytanych jest: ", elem.__len__()," ogłoszeń \n==========")


# przeszukujemy ogłoszenie w poszukiwaniu konkretnych elementów
for x in elem:
    print(" Tytuł:", x.find_element_by_class_name('css-wjfk7i').text, "\n",  #element znaleziony po nazwie klasy
          "Info:", x.find_element_by_class_name('css-jbk0sa').text, "\n", #element znaleziony po nazwie klasy
          "Płaca:", x.find_element_by_class_name('css-1dotj4s').text, "\n",#element znaleziony po nazwie klasy
          "Status:", x.find_element_by_class_name('css-hw5uoy').text, "\n==========")#element znaleziony po nazwie klasy
time.sleep(20)
driver.close()


