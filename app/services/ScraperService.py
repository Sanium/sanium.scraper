from time import sleep
from app.models.Job import Job
from app.services.SchedulerService import create_job


def main_page_job(*args, **kwargs):
    """
    Job function of scraping main page. It will by executed if user schedule scraping.
    """
    # TODO scrape main page
    # TODO save all found links
    # TODO schedule scraping for each link

    sleep(1)
    print('*** main_page_job ***')
    job_id = args[0]

    j: Job = Job.find(job_id)
    print(j.name, j.run_date)
    sleep(1)
    detail: Job = create_job('detail_page_job', detail_page_job, args=['conversion-it-project-manager-ecommerce'], seconds=15)
    print('detail run: ', detail.run_date)


def detail_page_job(*args, **kwargs):
    """
    Job function of scraping specified page with details about offer. It will be scheduled by main_page_job
    """
    # TODO scrape detail page
    # TODO save result in db as Offer

    job_id = args[0]
    j: Job = Job.find(job_id)
    print(j.name, j.run_date)
    sleep(1)
    site_id = args[1]
    print('site id:', site_id)
    sleep(1)
