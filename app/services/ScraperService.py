def main_page_job(*args, **kwargs):
    """
    Job function of scraping main page. It will by executed if user schedule scraping.
    """
    # TODO scrape main page
    # TODO save all found links
    # TODO schedule scraping for each link
    pass


def detail_page_job(*args, **kwargs):
    """
    Job function of scraping specified page with details about offer. It will be scheduled by main_page_job
    """
    # TODO scrape detail page
    # TODO save result in db as Offer
    pass
