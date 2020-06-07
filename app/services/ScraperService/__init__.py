from time import sleep

from app.models.Job import Job
from app.services.SchedulerService import create_job
from .Scraper import Scraper


def main_page_job(*args, **kwargs):
    """
    Job function of scraping main page. It will by executed if user schedule scraping.
    args = [job_id, website, offers_count_number]
    """
    print('*** main_page_job ***')

    # get args
    job_id = args[0]
    website = args[1]
    offers_count_number = args[2]

    j: Job = Job.find(job_id)

    # init scraper
    print('initializing scraper')
    scraper = Scraper(website)

    # run scrapping on main page
    print('scraping')
    scraper.run_main_page_scrapping(offers_count_number)

    # get basic offer data
    print('get data')
    data = scraper.get_data()

    print('saving')
    # scraper.save_data()

    print('creating details page jobs')
    seconds = 60
    for i in range(scraper.output.__len__()):
        offer_id = list(data.keys())[i]
        detail: Job = create_job('detail_page_job', detail_page_job, args=["https://justjoin.it/", offer_id],
                                 seconds=seconds)
        print('detail run: ', detail.run_date)
        seconds += 5
        sleep(1)


def detail_page_job(*args, **kwargs):
    """
    Job function of scraping specified page with details about offer. It will be scheduled by main_page_job
    args = [job_id, website, offer_id]
    """
    print('*** detail_page_job ***', args)
    job_id = args[0]
    website = args[1]
    offer_id = args[2]

    print('initializing scraper', job_id, website, offer_id)
    scraper = Scraper(website, debug=True)

    print('scraping')
    scraper.run_detail_page_scrapping(offer_id)

    print('saving')
    # scraper.save_data()  # save to file

    print('get data')
    scraper.get_data()  # get data as dict
    # TODO save result in db as Offer

    job_id = args[0]
    j: Job = Job.find(job_id)
    print(j.name, j.run_date)
    sleep(1)
    print('site id:', website)
    sleep(1)
