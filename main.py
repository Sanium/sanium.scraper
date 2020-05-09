import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from Scraper import Scraper


def main():
    scraper = Scraper()
    scraper.run("https://justjoin.it/", 100)  # działa tylko dla justjoin.it ;)


if __name__ == "__main__":
    main()
