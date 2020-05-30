from app.ScraperService.Scraper import Scraper


def main():
    scraper = Scraper()
    scraper.run_main_page_scrapping("https://justjoin.it/", 5)
    scraper.run_detail_page_scrapping()
    scraper.save_data()


if __name__ == "__main__":
    main()
