from .SchedulerService import scheduler, job_added_listener, job_executed_listener, job_submitted_listener
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ADDED, EVENT_JOB_SUBMITTED


def init_app(app):
    scheduler.init_app(app)
    scheduler.add_listener(job_added_listener, EVENT_JOB_ADDED)
    scheduler.add_listener(job_executed_listener, EVENT_JOB_EXECUTED)
    scheduler.add_listener(job_submitted_listener, EVENT_JOB_SUBMITTED)
    scheduler.start()
