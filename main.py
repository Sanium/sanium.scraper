from app.ScraperService.Scraper import Scraper

def main():
    scraper = Scraper("https://justjoin.it/")
    scraper.run_main_page_scrapping(5)

    s2 = Scraper("https://justjoin.it/")
    s2.run_detail_page_scrapping(list(scraper.get_data().keys())[0])
    s2.run_detail_page_scrapping(list(scraper.get_data().keys())[1])
    s2.run_detail_page_scrapping(list(scraper.get_data().keys())[2])
    s2.save_data()


if __name__ == "__main__":
    main()
