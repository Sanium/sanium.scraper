from time import sleep

from app.ScraperService.Scraper import Scraper
from app.models.Job import Job
from app.services.SchedulerService import create_job


def main_page_job(*args, **kwargs):
    """
    Job function of scraping main page. It will by executed if user schedule scraping.
    args = [job_id, website, offers_count_number]
    """
    # get args
    website = args[1]
    offers_count_number = args[2]

    # init scraper
    scraper = Scraper(website)

    # run scrapping on main page
    scraper.run_main_page_scrapping(offers_count_number)

    # get basic offer data
    data = scraper.get_data()

    scraper.save_data()

    # TODO schedule scraping for each link

    sleep(1)
    print('*** main_page_job ***')
    job_id = args[0]

    j: Job = Job.find(job_id)
    print(j.name, j.run_date)
    sleep(1)
    # TODO check
    for i in range(scraper.output.__len__()):
        offer_id = list(data.keys())[i]
        detail: Job = create_job('detail_page_job', detail_page_job, args=[i, "https://justjoin.it/", offer_id], seconds=15)
        print('detail run: ', detail.run_date)


def detail_page_job(*args, **kwargs):
    """
    Job function of scraping specified page with details about offer. It will be scheduled by main_page_job
    args = [job_id, website, offer_id]
    """
    website = args[1]
    offer_id = args[2]
    scraper = Scraper(website)

    scraper.run_detail_page_scrapping(offer_id)
    scraper.save_data()  # save to file
    scraper.get_data()  # get data as dict
    # TODO save result in db as Offer

    job_id = args[0]
    j: Job = Job.find(job_id)
    print(j.name, j.run_date)
    sleep(1)
    print('site id:', website)
    sleep(1)
