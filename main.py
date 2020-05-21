from Scraper import Scraper


def main():
    scraper = Scraper()
    scraper.run("https://justjoin.it/", 10)


if __name__ == "__main__":
    main()
