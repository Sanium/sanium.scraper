from app.services.ScraperService.Scraper import Scraper


def run_buldog():
    bulldog = {
        "service_name": "bulldogjob.pl",
        "main_page": {
            "url": "https://bulldogjob.pl/companies/jobs",
            "list_type": "pagination",
            "offer_list": {
                "by": "xpath",
                "locator": '//*[@id="search-result"]/div/section/ul'
            },
            "offer": {
                "by": "tag_name",
                "locator": "a"
            },
            "offer_title": {
                "by": "class_name",
                "locator": "title"
            },
            "offer_url": {
                "by": "tag_name",
                "locator": "a"
            }
        },
        "detail_page": {
            "offer_title": {
                "by": "xpath",
                "locator": '//*[@id="job-offer"]/div[2]/div[1]/div/div[2]/div[2]/h1'
            },
            "offer_technology": {
                "by": "xpath",
                "locator": '//*[@id="job-offer"]/div[2]/div[2]/div[1]/div[3]/div[5]/div[2]/div[1]/span/span'
            },
            "offer_salary": {
                "by": "class_name",
                "locator": 'salary'
            },
            "offer_salary_currency": {
                "by": "class_name",
                "locator": 'units'
            },
            "offer_location": {
                "by": "xpath",
                "locator": '//*[@id="job-offer"]/div[2]/div[1]/div/div[3]/div/div[3]/span/span'
            },
            "offer_experience": {
                "by": "xpath",
                "locator": '//*[@id="job-offer"]/div[2]/div[1]/div/div[2]/div[3]/strong'
            },
            "offer_employment": {
                "by": "xpath",
                "locator": '//*[@id="job-offer"]/div[2]/div[1]/div/div[3]/div/div[2]/span/span'
            },
            "offer_description": {
                "by": "xpath",
                "locator": '//*[@id="job-offer"]/div[2]/div[2]/div[1]/div[1]/div[2]'
            },
            "company_logo": {
                "by": "xpath",
                "locator": '//*[@id="job-offer"]/div[2]/div[2]/div[1]/div[1]/div[1]/a/img'
            },
            "company_name": {
                "by": "class_name",
                "locator": "company-name"
            },
        }
    }
    scraper = Scraper(service_struct=bulldog)
    scraper.run_main_page_scrapping(10)
    print(scraper.output)
    s2 = Scraper(service_struct=bulldog)
    for k in list(scraper.get_data().keys()):
        s2.run_detail_page_scrapping(k)
    print(s2.output)
    # s2.save_data()

def run_jjit():
    scraper = Scraper(website='https://justjoin.it/')
    scraper.run_main_page_scrapping(10)
    print(scraper.output)
    s2 = Scraper(website='https://justjoin.it/')
    for k in list(scraper.get_data().keys()):
        s2.run_detail_page_scrapping(k)
    print(s2.output)

def main():
    # run_jjit()
    run_buldog()

if __name__ == "__main__":
    print("dupa")
